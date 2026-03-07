import asyncio
import httpx

# 请替换成你的实际 IP 和端口

BASE_URL="http://10.160.108.2:11434/v1"
MODEL="qwen3-vl:8b"

SERVER_URL = "http://10.160.108.2:11434/v1/chat/completions"


async def ask_my_qwen(prompt):
    payload = {
        "model": MODEL,  # 根据你的实际模型名称修改
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    print(f"📡 正在向服务器发送请求：{prompt}")

    # ------------------------------------------------
    # 👇 填空 1：我们需要在这里使用 httpx 的异步客户端，
    # 并且要用到“异步上下文管理器”来确保请求结束后自动关闭连接。
    # ------------------------------------------------
    async with httpx.AsyncClient(trust_env=False) as client:

        # ------------------------------------------------
        # 👇 填空 2：发送 POST 请求是一个耗时的网络 I/O 操作。
        # 这里需要用哪个关键字来挂起任务等待响应？
        # ------------------------------------------------
        # 👇 你填写的正确代码
        response = await client.post(SERVER_URL, json=payload, timeout=30.0)

        # ------------------------------------------------
        # 🕵️‍♂️ 新增调试代码：检查 HTTP 状态码
        # ------------------------------------------------
        if response.status_code != 200:
            print(f"❌ 服务器打回了我们的请求，状态码: {response.status_code}")
            print(f"📄 服务器说: {response.text}")
            return "抱歉，请求失败了"

        # 解析返回的 JSON 数据
        result = response.json()
        return result["choices"][0]["message"]["content"]


async def main():
    try:
        reply = await ask_my_qwen("你好，请用一句话介绍一下你自己。")
        print(f"\n🤖 Qwen 的回答：{reply}")
    except Exception as e:
        # type(e).__name__ 可以打印出是 ConnectError 还是 KeyError
        print(f"❌ 运行出错了！错误类型：{type(e).__name__}，详细信息：{e}")


# 启动事件循环
asyncio.run(main())