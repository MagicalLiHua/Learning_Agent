import asyncio
import functools
import random


def async_retry(max_retries=3, backoff_factor=2):
    """
    一个通用的异步重试装饰器
    """

    def decorator(func):
        @functools.wraps(func)  # 保持原函数的元数据（如名字、文档字符串）
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    # 核心：在这里 await 原函数
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    wait_time = (attempt + 1) * backoff_factor
                    print(f"⚠️ [尝试 {attempt + 1}] {func.__name__} 出错: {e}。{wait_time}s 后重试...")
                    await asyncio.sleep(wait_time)

            print(f"❌ {func.__name__} 在 {max_retries} 次尝试后仍然失败。")
            raise last_exception

        return wrapper

    return decorator


# --- 使用方式 ---

@async_retry(max_retries=3, backoff_factor=1)
async def call_llm_api(model_name):
    print(f"🚀 正在请求 {model_name}...")
    if random.random() < 0.8:  # 80% 概率失败
        raise ConnectionError("API 暂时不可用")
    return "这是模型返回的精彩答案"


async def main():
    try:
        result = await call_llm_api("GPT-4o")
        print(f"✅ 成功结果: {result}")
    except Exception:
        print("🙏 最终还是没辙了")


asyncio.run(main())