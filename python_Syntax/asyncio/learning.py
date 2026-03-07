import asyncio


async def fetch_data():
    print("开始下载数据...")
    # 模拟一个耗时的网络请求
    await asyncio.sleep(2)
    print("数据下载完成！")
    return {"data": 123}

# 如果我直接这样调用：
result = fetch_data()
print(result)