import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import SseServerParams
from autogen_ext.tools.mcp import mcp_server_tools
from loguru import logger


async def main() -> None:
    logger.debug("Starting main function...")
    model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key="sk-bf45e97095c64d8aa0336a7857563493",
        base_url="https://api.deepseek.com",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.ANY,
            "structured_output": True,
        },
    )
    server_params = SseServerParams(url="http://127.0.0.1:8000/sse")
    tools = await mcp_server_tools(server_params)

    agent_a = AssistantAgent("A", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="你可以构思一个故事，给出一个标题和关键点。")
    agent_b = AssistantAgent("B", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="根据标题和关键点，请你使用自己方式1写")
    agent_c = AssistantAgent("C", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="根据标题和关键点，请你使用自己方式2写")
    agent_d = AssistantAgent("D", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="总结哪个写的更好，更加适合5-7岁小孩？输出必须包含结束符号||||||")

    builder = DiGraphBuilder()
    builder.add_node(agent_a).add_node(agent_b).add_node(agent_c).add_node(agent_d)
    builder.add_edge(agent_a, agent_b).add_edge(agent_a, agent_c).add_edge(agent_b, agent_d).add_edge(agent_c, agent_d)
    graph = builder.build()

    team = GraphFlow(
        participants=[agent_a, agent_b, agent_c, agent_d],
        graph=graph,
        termination_condition=TextMessageTermination('||||||'),
    )

    async for event in team.run_stream(task="写一个关于几何的教程，需要包含圆的面积。直径为100，面积为多少？"):
        print(event)


asyncio.run(main())
