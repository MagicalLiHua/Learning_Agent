import asyncio

# 注意：这里是 async def 且里面有 yield
async def llm_stream_generator(prompt):
    words = [f"收到 {prompt}，", "这是", "我", "给", "你", "的", "回答。"]
    for word in words:
        await asyncio.sleep(0.3) # 模拟每 0.3 秒生成一个词
        yield word  # 异步产出一个词

async def main():
    # 异步迭代器需要用 async for
    async for chunk in llm_stream_generator("你好呀"):
        print(chunk, end="", flush=True)

asyncio.run(main())