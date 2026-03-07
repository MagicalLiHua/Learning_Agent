import asyncio

async def call_very_slow_llm():
    await asyncio.sleep(10)  # 模拟一个超级慢的响应
    return "终于算完了"

async def main():
    try:
        # 设置 2 秒超时
        result = await asyncio.wait_for(call_very_slow_llm(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("⏰ 报错：模型响应太慢，我们不等了！")

asyncio.run(main())