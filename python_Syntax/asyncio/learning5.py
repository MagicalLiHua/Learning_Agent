import asyncio
import httpx
import time


async def ask_model(client, model_name, prompt):
    print(f"[{model_name}] 正在思考...")
    # 模拟发送请求到不同的 API 节点
    # 在实际开发中，这里会是 client.post("https://api.openai.com/...", ...)
    response = await client.get("https://httpbin.org/delay/2")
    print(f"[{model_name}] 回答完毕！")
    return f"{model_name} 的结果"


async def main():
    # 使用 AsyncClient 维护连接池，效率极高
    async with httpx.AsyncClient() as client:
        tasks = [
            ask_model(client, "GPT-4o", "什么是异步编程？"),
            ask_model(client, "Claude-3.5", "什么是异步编程？"),
            ask_model(client, "DeepSeek-V3", "什么是异步编程？"),
        ]

        start = time.perf_counter()
        # 并发执行
        results = await asyncio.gather(*tasks)
        end = time.perf_counter()

        print(f"\n最终汇总: {results}")
        print(f"总计耗时: {end - start:.2f}s (如果是同步请求则需要 6s+)")


if __name__ == "__main__":
    asyncio.run(main())