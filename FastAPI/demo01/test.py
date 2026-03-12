import requests

# 你的 FastAPI 服务的地址
API_URL = "http://127.0.0.1:8000/chat"


def ask_customer_service(user_id, text):
    # 构建发送给 API 的 JSON 数据
    payload = {
        "question": text,
        "session_id": user_id  # 根据不同的用户传入不同的 ID
    }

    print(f"\n[{user_id}] 发送请求中...")

    # 向 API 发送 POST 请求
    response = requests.post(API_URL, json=payload)

    # 解析 API 返回的 JSON 结果
    if response.status_code == 200:
        result = response.json()
        print(f"客服回复: {result['answer']}")
    else:
        print(f"请求失败，状态码: {response.status_code}")


# --- 测试多用户场景 ---

# 模拟用户 张三 连续提问（测试历史记忆）
ask_customer_service(user_id="zhangsan_01", text="我要怎么申请退款？")
ask_customer_service(user_id="zhangsan_01", text="我申请退款被商家拒绝了怎么办？")

# 模拟用户 李四 提问（测试用户隔离，李四不会知道张三点了炸鸡）
ask_customer_service(user_id="lisi_99", text="外卖申请退款但是被商家拒绝了怎么办")