import asyncio
import warnings

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

warnings.filterwarnings('ignore')


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key="sk-bf45e97095c64d8aa0336a7857563493",
        base_url="https://api.deepseek.com",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.ANY,
            "structured_output": False,
        },
    )

    blog_writer = AssistantAgent(
        name="BlogWriter",
        model_client=model_client,
        system_message="你是一个专业的博客文章生成器，针对给定主题生成一段文章。",
        description="生成一段博客文章。"
    )

    hashtag_generator = AssistantAgent(
        name="HashtagGenerator",
        model_client=model_client,
        system_message="你为给定的主题或内容生成 3 个相关的 hashtags。",
        description="根据输入内容生成 hashtags。"
    )

    team = MagenticOneGroupChat([blog_writer, hashtag_generator], model_client=model_client)

    task = "撰写一篇关于人工智能在教育中好处的短篇博客文章，并生成相关的 hashtags。"
    await Console(team.run_stream(task=task))

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
