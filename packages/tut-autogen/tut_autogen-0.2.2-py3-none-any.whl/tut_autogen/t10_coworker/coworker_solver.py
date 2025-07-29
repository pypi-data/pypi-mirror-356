import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import SseServerParams
from autogen_ext.tools.mcp import mcp_server_tools
from loguru import logger


async def init_resources():
    """Initialize reusable resources."""
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
    logger.info(f"Initialized {len(tools)} tools")

    agent_a = AssistantAgent("A", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="你是一个解决问题的高手，你可以对问题进行分解。")
    agent_b = AssistantAgent("B", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="你对分解的问题进行逐一回答，给给出最终答案。")
    agent_c = AssistantAgent("C", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="你对分解的问题进行逐一回答，给给出最终答案。")
    agent_d = AssistantAgent("D", model_client=model_client, reflect_on_tool_use=True, tools=tools, system_message="上述哪个回答的更好呢？||||||")

    return {
        'model_client': model_client,
        'tools': tools,
        'agent_a': agent_a,
        'agent_b': agent_b,
        'agent_c': agent_c,
        'agent_d': agent_d
    }


async def create_team(agent_a, agent_b, agent_c, agent_d):
    """Create a new GraphFlow team."""
    builder = DiGraphBuilder()
    builder.add_node(agent_a).add_node(agent_b).add_node(agent_c).add_node(agent_d)
    builder.add_edge(agent_a, agent_b).add_edge(agent_a, agent_c).add_edge(agent_b, agent_d).add_edge(agent_c, agent_d)
    graph = builder.build()
    team = GraphFlow(
        participants=[agent_a, agent_b, agent_c, agent_d],
        graph=graph,
        termination_condition=TextMessageTermination('||||||'),
    )
    return team


async def process_task(team, task: str):
    """Process a single task."""
    result = None
    try:
        async with asyncio.timeout(60):
            async for event in team.run_stream(task=task):
                if isinstance(event, TaskResult):
                    for message in event.messages:
                        logger.info(f">>>> {message}")
                        if '真值标定回答完成' in str(message):
                            result = message.content
                            logger.info(f">>>> {result['ground_truth']}")
                            return result
    except asyncio.TimeoutError:
        logger.error(f"Task timed out: {task}")
    except Exception as e:
        logger.exception(f"Error processing task: {task}, Error: {e}")
    finally:
        await team.reset()
    return result


async def main() -> None:
    logger.debug("Starting main function...")

    resources = await init_resources()

    tasks = [
        "成语 “朝三暮四” 原指猴子被骗，早上给 3 颗栗子，晚上给 4 颗；后改为早上 4 颗，晚上 3 颗。若每颗栗子热量为 20 千卡，猴子每天进食热量不变，且 1 千卡≈4.18 千焦。当猴子改为 “朝四暮三” 后，其早餐热量比之前增加多少千焦？",
        "月球表面昼夜温差约 300℃（-180℃~120℃），水的沸点随气压降低而下降，已知月球表面气压约为地球的 1/10^14。若在地球标准大气压下水沸点为 100℃，且每降低 1 个数量级气压，沸点下降约 3℃，求月球表面 “理论沸点”。",
        "郑和七下西洋最远到达非洲东海岸，已知明朝船队平均航速约为 15 海里 / 小时，单次航程约需 3 个月（每月按 30 天计）。若地球赤道周长约 40075 公里，1 海里≈1.852 公里，郑和船队单程航行距离占赤道周长的百分之多少？（保留整数）",
        "DNA 双螺旋结构可视为拓扑学中的环面（Torus），若某段 DNA 含 1000 个碱基对，每 10 个碱基对形成一个螺旋（螺距 3.4nm）。当 DNA 发生拓扑异构时，每增加 1 个超螺旋会减少 1 个连环数（Linking number）。若该 DNA 初始连环数为 100，被拓扑异构酶 Ⅱ 引入 3 个正超螺旋，求此时 DNA 的螺旋长度与初始长度的比值（保留 3 位小数）。",
    ]

    for task in tasks:
        logger.debug(f"Processing task: {task}")
        try:
            team = await create_team(resources['agent_a'], resources['agent_b'], resources['agent_c'], resources['agent_d'])
            result = await process_task(team, task)
            if result:
                print(result)
        except Exception as e:
            logger.exception(f"Error in task: {task}, Error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception("Program interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error in main: {e}")
