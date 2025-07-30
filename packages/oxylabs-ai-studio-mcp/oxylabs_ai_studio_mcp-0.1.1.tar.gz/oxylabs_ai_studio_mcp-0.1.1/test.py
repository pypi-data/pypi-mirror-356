import os
import asyncio

from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic_ai.mcp import MCPServerStdio

import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
# server = MCPServerStdio(  
#     'uv',
#     args=[
#           '--directory',
#           '/Users/T220908/Desktop/oxybrain/oxylabs-studio/github/oxylabs-ai-studio-mcp-py',
#           "run",
#           'oxylabs-ai-studio-mcp'
#     ],
#     env={
#         "OXYLABS_AI_STUDIO_API_KEY": os.environ["OXYLABS_AI_STUDIO_API_KEY"],
#     },
#     # log_level="debug",
# )

server = MCPServerStdio(  
    'uvx',
    args=[
          'oxylabs-ai-studio-mcp',
          '--default-index',
          'https://test.pypi.org/simple/',
          '--index',
          'https://pypi.org/simple',
    ],
    env={
        "OXYLABS_AI_STUDIO_API_KEY": os.environ["OXYLABS_AI_STUDIO_API_KEY"],
        "OXYLABS_AI_STUDIO_API_URL": os.environ["OXYLABS_AI_STUDIO_API_URL"],
    },
    # log_level="debug",
)

# requires OPENAI_API_KEY to be set.
agent = Agent('openai:gpt-4o', mcp_servers=[server])


async def main():
   
    async with agent.run_mcp_servers():
        print("started")
        # print(await server.list_tools())
        result = await agent.run('find me some lasagna recipes.')
        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())