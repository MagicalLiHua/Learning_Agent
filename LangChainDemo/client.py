from loguru import logger
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    """
    MCP客户端类，用于管理与MCP服务器的连接和交互

    该类负责初始化客户端会话、处理聊天循环以及资源清理
    """

    def __init__(self):
        """
        初始化MCP客户端实例

        初始化客户端会话、异步退出栈和Anthropic客户端
        """
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_mock_server(self):
        """
        连接到模拟服务器

        当前实现仅记录初始化信息，未实际建立服务器连接
        """
        logger.info("✅ MCP 客户端已初始化，但未连接到服务器")

    async def chat_loop(self):
        """
        运行聊天循环

        持续接收用户输入并显示回显，直到用户输入'quit'退出
        支持异常处理以确保程序稳定性
        """
        logger.info("MCP 客户端已启动！")
        print("输入你的问题或输入 'quit' 退出。")

        # 主聊天循环
        while True:
            try:
                query = input("\n🧑‍🦲 [用户输入]: ").strip()

                # 检查退出条件
                if query.lower() == 'quit':
                    break

                # 显示用户输入作为AI回答（模拟响应）
                print(f"\n🤖 [AI回答] ：{query}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """
        清理资源

        关闭异步退出栈中管理的所有资源
        """
        await self.exit_stack.aclose()


async def main():
    """
    主函数，程序入口点

    创建MCP客户端实例，建立连接并启动聊天循环，最后进行资源清理
    """
    client = MCPClient()
    try:
        await client.connect_to_mock_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


# 使用asyncio.run()来运行异步主函数main()，确保了异步程序能够正确启动和执行
if __name__ == "__main__":
    asyncio.run(main())