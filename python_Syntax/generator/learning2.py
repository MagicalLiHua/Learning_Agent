def llm_processor():
    temp = 0.7  # 默认温度
    print(f"当前初始温度设定为: {temp}")

    while True:
        # yield 产出当前状态，并等待外部传回新的温度
        new_temp = yield f"使用温度 {temp} 处理中..."

        if new_temp is not None:
            print(f"--- 收到指令：将温度从 {temp} 修改为 {new_temp} ---")
            temp = new_temp

proc = llm_processor()
print(next(proc))  # 启动生成器，输出初始状态

print(proc.send(0.9))  # 发送新的温度，输出更新后的状态