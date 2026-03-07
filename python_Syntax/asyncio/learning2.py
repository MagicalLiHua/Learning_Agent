import asyncio
import time

async def call_llm(name, delay):
    print(f"--- 🚀 正在请求模型 {name} ...")
    # 模拟网络延迟，这不会阻塞整个程序
    await asyncio.sleep(delay)
    print(f"--- ✅ 模型 {name} 响应完成！")
    return f"{name} 的回答内容"

async def main():
    start_time = time.perf_counter()

    print("开始并发调用...")
    # asyncio.gather 会同时提交多个任务到事件循环
    # 就像同时派出了 3 个服务员去不同的桌子取餐
    results = await asyncio.gather(
        call_llm("GPT-4", 3),
        call_llm("Claude-3", 2),
        call_llm("Llama-3", 1)
    )

    end_time = time.perf_counter()
    print(f"\n全部结果: {results}")
    print(f"总耗时: {end_time - start_time:.2f} 秒")

# 启动导演（事件循环）
asyncio.run(main())