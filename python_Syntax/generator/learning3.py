def sub_task():
    feedback = yield "子任务开始"
    print(f"子任务收到: {feedback}")

def main_manager():
    yield from sub_task()

mgr = main_manager()
print(next(mgr))      # 输出: "子任务开始"
mgr.send("来自总控的指令") # 猜猜这个指令飞到哪里去了？