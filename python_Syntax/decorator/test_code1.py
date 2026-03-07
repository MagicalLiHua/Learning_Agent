import functools


def retry(max_retries=3):

    def decorator(func):

        # 抛出最后一次异常
        # 保留被装饰函数的元数据
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {i+1} 次尝试失败: {e}")
                    if i == max_retries - 1:
                        raise
                    else:
                        print("正在重试...")
        return wrapper

    return decorator

@retry(max_retries=5)
def unstable_function():
    import random
    if random.random() < 0.7:  # 70% 的概率抛出异常
        raise ValueError("函数执行失败！")
    return "函数执行成功！"

if __name__ == "__main__":
    print(unstable_function.__name__)

