import asyncio
import warnings
from datetime import datetime

import pandas as pd
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base._task import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import SseServerParams
from autogen_ext.tools.mcp import mcp_server_tools
from loguru import logger

from tut_autogen.t8_ground_truth_generator.promopts import *

warnings.filterwarnings('ignore')


async def initialize_resources():
    """初始化所有可复用的资源"""
    server_params = SseServerParams(url="http://127.0.0.1:8000/sse")
    tools = await mcp_server_tools(server_params)
    logger.info(f"Initialized {len(tools)} tools")

    custom_model_client = OpenAIChatCompletionClient(
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

    termination = TextMentionTermination("真值标定回答完成")
    agent = AssistantAgent(
        name="tool_user",
        model_client=custom_model_client,
        tools=tools,
        system_message=system_message_a
    )

    team = RoundRobinGroupChat([agent], termination_condition=termination)

    return {
        'tools': tools,
        'model_client': custom_model_client,
        'termination': termination,
        'agent': agent,
        'team': team
    }


async def process_task(team, task: str) -> dict:
    """处理单个任务"""
    result = {}
    async for event in team.run_stream(task=task):
        if isinstance(event, TaskResult):
            for message in event.messages:
                if '真值标定回答完成' in str(message):
                    result = {
                        'questions': task,
                        'ground_truth': str(message.content)
                    }
                    logger.info(f">>>> 【【{result['ground_truth']}】】")
    return result


async def main() -> None:
    # 一次性初始化所有资源
    resources = await initialize_resources()
    df = pd.read_csv("questions.csv")
    logger.info(f"Loaded CSV with {len(df)} rows")

    results = []
    for idx, row in df.iterrows():
        try:
            task = row['问题集合']
            start_time = datetime.now()

            task_result = await process_task(resources['team'], task)

            if task_result:
                results.append(task_result)

            await resources['team'].reset()

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Task {idx} completed in {duration:.2f} seconds")
        except Exception as e:
            logger.exception(f"Error in task {idx}, {row.values}: {e}")
        # 注意：这里移除了break，以便处理所有行

    pd.DataFrame(results).to_csv("ground_truth.csv", index=False)
    logger.info(f"Saved {len(results)} results to ground_truth.csv")


if __name__ == '__main__':
    asyncio.run(main())
