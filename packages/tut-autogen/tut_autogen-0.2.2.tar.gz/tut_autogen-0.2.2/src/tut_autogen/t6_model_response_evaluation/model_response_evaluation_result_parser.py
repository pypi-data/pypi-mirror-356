import asyncio
import json
import re
import typing
import warnings
from typing import Dict, Any

import pandas as pd
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base._task import TaskResult
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from loguru import logger

from prompts import *

warnings.filterwarnings('ignore')


def clean_think_tags(docstring):
    """
    清除docstring中所有的<think>...</think>标签内容
    """
    if not docstring:
        return docstring
    return re.sub(r'<think>.*?</think>', '', docstring, flags=re.DOTALL)


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    从包含JSON的文本中提取JSON结构
    :param text: 包含JSON的原始文本
    :return: 解析后的字典对象
    """
    text = clean_think_tags(text).strip()
    json_match = re.search(r'\{[\s\S]*\}', text)
    if not json_match:
        logger.error(f"No valid JSON structure found in text: {text}")
        return {"error": "No valid JSON structure found"}

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {str(e)}, text: {text}")
        return {"error": f"JSON parsing failed: {str(e)}"}


async def run_task(team, task, q, r, gt):
    """
    运行单个任务并处理结果
    :param team: GraphFlow 团队
    :param task: 任务字符串
    :param q: 查询
    :param r: 模型回答
    :param gt: 标准答案
    :return: 处理后的结果字典
    """
    result = {"query": q, "response": r, "ground_truth": gt}
    try:
        # 收集所有消息，确保生成器完全消耗
        messages = []
        async for event in team.run_stream(task=task):
            if isinstance(event, TextMessage):
                logger.debug(f"Message received: {event}")
                messages.append(event)
            if isinstance(event, TaskResult):
                logger.debug(f"Task completed: {event}")
                messages = event.messages
                break
        else:
            logger.warning(f"Task did not complete with TaskResult, messages: {messages}")

        # 从代理 C 的消息中提取结果
        for message in messages:
            if message.source == "C":
                try:
                    target_message = extract_json_from_text(message.content)
                    if "error" in target_message:
                        result.update({"error": target_message["error"]})
                        result.update({"conclusion": target_message})
                    else:
                        conclusion = target_message.get("conclusion", "No conclusion found")
                        if conclusion == "No conclusion found":
                            conclusion = target_message
                        result.update({"conclusion": conclusion})
                except Exception as e:
                    logger.error(f"Failed to process message from C: {str(e)}")
                    result.update({"error": f"Message processing failed: {str(e)}"})
                break
        else:
            logger.warning(f"No message from agent C for query: {q}")
            result.update({"error": "No response from agent C"})

        return result
    except Exception as e:
        logger.error(f"Task failed for query {q}: {str(e)}")
        result.update({"error": f"Task execution failed: {str(e)}"})
        return result


async def main() -> None:
    logger.debug("Starting main function...")
    model_client = OpenAIChatCompletionClient(
        model="Qwen3-235B-A22B",
        api_key="LanzOpenAI_54a27832-d574-4c6e-80f5-2de174d0ae49",
        base_url="http://lanz.hikvision.com/v3/openai/qwen3-235b-a22b",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.ANY,
            "structured_output": True,
        },
    )

    # 读取 CSV 文件
    try:
        df = pd.read_csv("model_response_evaluation.csv")
        logger.info(f"Loaded CSV with {len(df)} rows")
    except Exception as e:
        logger.error(f"Failed to load CSV: {str(e)}")
        logger.info(f"错误: 无法加载 CSV 文件 - {str(e)}")
        return

    results = []

    for idx, row in df.iterrows():
        idx = typing.cast(int, idx)
        try:
            q, r, gt = row
            logger.debug(f"Processing row {idx + 1}: query={q}, response={r}, ground_truth={gt}")
            task = user_prompt.substitute(query=q, response=r, ground_truth=gt)

            # 为每个任务创建新的 GraphFlow 实例
            agent_a = AssistantAgent("A", model_client=model_client, system_message=system_message_a)
            agent_b = AssistantAgent("B", model_client=model_client, system_message=system_message_b)
            agent_c = AssistantAgent("C", model_client=model_client, system_message=system_message_c)

            builder = DiGraphBuilder()
            builder.add_node(agent_a).add_node(agent_b).add_node(agent_c)
            builder.add_edge(agent_a, agent_b).add_edge(agent_b, agent_c)
            graph = builder.build()

            team = GraphFlow(
                participants=[agent_a, agent_b, agent_c],
                graph=graph,
                termination_condition=TextMessageTermination("总结结束"),
            )

            # 运行任务
            logger.info(f">>>>>> Running task {idx} for query: {q}")
            result = await run_task(team, task, q, r, gt)
            results.append(result)

            # 打印当前结果
            logger.debug(f"问题: {q}")
            logger.success(f"判断: {result}")
            logger.success("<<<<<< 任务已经完成.")

        except Exception as e:
            logger.error(f"Error processing row {idx + 1}: {str(e)}")
            q, r, gt = row
            results.append({
                "query": q,
                "response": r,
                "ground_truth": gt,
                "error": f"Row processing failed: {str(e)}"
            })

    # 保存结果到 CSV
    try:
        pd.DataFrame(results).to_csv("model_response_evaluation_result.csv", index=False)
        logger.info("Results saved to model_response_evaluation_result.csv")
    except Exception as e:
        logger.error(f"Failed to save results to CSV: {str(e)}")
        logger.error(f"错误: 无法保存结果到 CSV - {str(e)}")


if __name__ == '__main__':
    asyncio.run(main())
