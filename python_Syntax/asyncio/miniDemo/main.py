import functools


def get_texts_to_translate():
    """
    这是一个普通的生成器函数。
    它的任务是一次提供一句话。
    """
    sentences = [
        "你好",
        "异步编程很有趣",
        "大语言模型改变了世界"
    ]

    for sentence in sentences:
        yield sentence

def async_retry(max_retries=3, backoff_factor=1):
    """
    这是一个装饰器工厂函数。
    它返回一个装饰器，装饰器会在被装饰的异步函数发生异常时自动重试。
    """
    def decorator(func):
        @functools.wraps(func)  # 保持原函数的元数据（如名字、文档字符串）
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ 出现错误: {e}，正在重试... (第 {retries + 1} 次)")
                    retries += 1
                    await asyncio.sleep(backoff_factor * retries)  # 指数退避
            raise Exception(f"❌ 重试失败: 已经尝试了 {max_retries} 次。")
        return wrapper
    return decorator


import asyncio
import random


@async_retry(max_retries=3, backoff_factor=1)
async def translate_text(text):
    print(f"🚀 正在发送给 LLM 翻译: '{text}'")

    # 模拟 50% 的概率网络崩溃，触发我们的装饰器重试
    if random.random() < 0.5:
        raise ConnectionError("哎呀，网络波动了！")

    await asyncio.sleep(1)

    return f"【已翻译】{text}"


async def main():
    # 1. 从生成器中获取所有句子
    sentences = list(get_texts_to_translate())

    # 2. 为每一句话生成一个异步任务（此时还没开始跑）
    tasks = [translate_text(sentence) for sentence in sentences]

    print("--- 🌟 开始高并发批量翻译 ---")

    results = await asyncio.gather(*tasks, return_exceptions=True)

    print("\n--- ✅ 翻译任务全部结束 ---")
    for res in results:
        print(res)

# ------------------------------------------------
# 👇 填空 4：最后一步，我们需要启动“事件循环”这位导演。
# 应该用什么代码来运行 main() 函数？
# ------------------------------------------------
asyncio.run(main())