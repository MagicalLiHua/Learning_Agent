import asyncio
from langchain_ollama import ChatOllama

# 设置本地模型
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")


async def main():
    # 1. 创建任务一（任务立即开始并在后台运行，不会阻塞下一行）
    task1 = asyncio.create_task(model.ainvoke("解释一下LangChain是什么"))

    # 2. 创建任务二（紧接着开始，现在后台有两个请求在跑了）
    task2 = asyncio.create_task(model.ainvoke("什么是异步编程？"))

    # 3. 这句代码会立刻执行，不会等大模型返回
    print("--- 提示：两个大模型请求已并发发出，正在排队处理中... ---")

    # 你甚至可以在这里做其他耗时操作
    print("主程序正在处理其他本地逻辑...")
    await asyncio.sleep(1)

    # 4. 获取结果：当我们真的需要结果时，再 await 任务对象
    # 如果此时模型已经返回，await 会立即拿到值；如果还没回，就在这里等。
    response1 = await task1
    print("\n[任务 1 返回了]")

    response2 = await task2
    print("\n[任务 2 返回了]")

    # 打印部分内容查看
    print("-" * 20)
    print(f"回答1摘要: {response1.content[:50]}...")
    print(f"回答2摘要: {response2.content[:50]}...")


# 运行
if __name__ == "__main__":
    asyncio.run(main())