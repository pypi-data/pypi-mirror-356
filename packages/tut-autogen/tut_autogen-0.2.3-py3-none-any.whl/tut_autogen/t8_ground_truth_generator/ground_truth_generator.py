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

from prompts import *

warnings.filterwarnings('ignore')


async def main() -> None:
    server_params = SseServerParams(url="http://127.0.0.1:8000/sse")
    tools = await mcp_server_tools(server_params)
    logger.info(f"tools: {len(tools)}")
    custom_model_client = OpenAIChatCompletionClient(
        model="Qwen3-235B-A22B",
        api_key="",
        base_url="http://lanz.hikvision.com/v3/openai/qwen3-235b-a22b",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.ANY,
            "structured_output": True,
        },
    )

    df = pd.read_csv("questions.csv")
    logger.info(f"Loaded CSV with {len(df)} rows")

    results = []
    for idx, row in df.iterrows():
        try:
            task = row['问题集合']
            start_time = datetime.now()

            termination = TextMentionTermination("真值标定回答完成")
            agent = AssistantAgent(name="tool_user", model_client=custom_model_client, tools=tools, system_message=system_message_a)
            team = RoundRobinGroupChat([agent], termination_condition=termination)

            async for event in team.run_stream(task=task):
                if isinstance(event, TaskResult):
                    for message in event.messages:
                        if str(message).__contains__('真值标定回答完成'):
                            result = str(message.content)
                            results.append({'questions': task, 'ground_truth': result})
                            logger.info(f">>>> 【【{result}】】")
                            logger.info(f">>>> {type(result)}")
                            logger.info(f">>>> {str(message).__contains__('真值标定回答完成')}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Task {idx} completed in {duration:.2f} seconds")
        except Exception as e:
            logger.exception(f"Error in task {idx}, {row.values}: {e}")
        break
    pd.DataFrame(results).to_csv("ground_truth.csv", index=False)
    logger.info("Results saved to ground_truth.csv")


if __name__ == '__main__':
    asyncio.run(main())
