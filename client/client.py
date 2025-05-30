import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        # self.anthropic = Anthropic()

    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command="python",
            args=["/home/lxwang12/opensource/zwppt-mcp/src/zwppt_mcp/server.py"],
            env={
                "AIPPT_APP_ID":"dcda0541",
                "AIPPT_API_SECRET":"ODA3MjkzZTllYmRlYzliY2Q5NjYxMmRj"
            }
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

    async def list_tools(self):
        response = await self.session.list_tools()
        tools = response.tools
        return tools

    async def call_tool(self, tool_name: str, arguments: dict):
        result = await self.session.call_tool(tool_name, arguments)
        return result

    async def close(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()

        tools = await client.list_tools()
        print("Connected to server with tools:", [tool.name for tool in tools])

        # result = await client.call_tool("get_theme_list", arguments={})
        # print("Result of get_theme_list:", result)

        # result = await client.call_tool("create_ppt_task", arguments={"text": "人工智能发展历程","template_id": "202407179097C2D"})
        # print("Result of create_ppt_task:", result)

        # result = await client.call_tool("get_task_progress", arguments={"sid": "329cb01641314eccbdc05266e0047dcd"})
        # print("Result of get_task_progress:", result)

        # result = await client.call_tool("create_outline", arguments={"text": "人工智能发展历程","search": False, "language": "cn"})
        # print("Result of create_outline:", result)

        # result = await client.call_tool("create_outline_by_doc", arguments={"file_name": "人工智能发展历程","text": "1"})
        # print("Result of create_outline_by_doc:", result)

        # result = await client.call_tool("create_ppt_by_outline", arguments={"text": "人工智能发展历程","search": False, "language": "cn"})
        # print("Result of create_ppt_by_outline:", result)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())