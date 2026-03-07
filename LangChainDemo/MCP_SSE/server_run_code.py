import asyncio
from mcp.server.fastmcp import FastMCP

# 创建实例
mcp = FastMCP("AsyncCodeRunner", host="0.0.0.0", port=8001)

@mcp.tool()
async def run_python_script(code: str) -> str:
    """
    异步执行 Python 代码。
    这样即使代码跑很久，也不会阻塞服务器的其他功能。
    """
    try:
        # 1. 创建子进程 (相当于雇个人去跑代码)
        # 这里不使用 subprocess.run，而是使用 asyncio 的方法
        process = await asyncio.create_subprocess_exec(
            "python", "-c", code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 2. 等待结果 (await)
        # 关键点：在等待的时候，主线程可以去干别的事（比如响应心跳包、处理其他请求）
        # communicate() 会读取标准输出和错误输出
        stdout, stderr = await process.communicate()

        # 3. 解码结果
        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if process.returncode == 0:
            return f"运行成功 ✅\n输出:\n{output}"
        else:
            return f"运行报错 ❌\n错误:\n{error}"

    except Exception as e:
        return f"系统执行异常: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")