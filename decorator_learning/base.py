def log(func):
    def wrapper(*args, **kwargs):
        print("正在执行函数：", func.__name__)
        # 调用原始函数，并传递参数
        # 这里的*args和**kwargs是为了支持任意数量的位置参数和关键字参数，确保装饰器可以适用于各种函数。
        # 自动解包参数，*args会将位置参数解包成一个元组，**kwargs会将关键字参数解包成一个字典，这样就可以将这些参数传递给原始函数。
        value = func(*args, **kwargs)
        print("函数执行完毕")
        return value
    return wrapper

@log # 原理 send_mail = log(send_mail)
# 通过装饰器的方式来调用函数，装饰器会在函数执行前后添加一些额外的功能
# 本质上是闭包的一种应用，装饰器函数接受一个函数作为参数，并返回一个新的函数，这个新函数在执行时会调用原始函数，并在其前后添加一些额外的功能。
def send_wechat(receiver, message):
    print(f"发送微信:{message} 给{receiver}")
    return 200

@log
def send_file(file_path):
    print(f"发送文件: {file_path}")


# 定义主函数调用几个方法
if __name__ == "__main__":
    result =  send_wechat("李华","Hello, World!")
    print("函数返回值：", result)

    send_file("/path/to/file.txt")