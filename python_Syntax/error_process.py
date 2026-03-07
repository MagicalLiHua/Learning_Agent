import os


def safe_file_reader(filename):
    """
    尝试读取文件内容，演示 try-except-else-finally 的完整流程
    """
    f = None  # 初始化变量，防止 finally 中访问不到

    print(f"\n--- 开始尝试读取: {filename} ---")

    try:
        # 1. 尝试执行高风险操作
        # open() 可能会抛出 FileNotFoundError
        f = open(filename, 'r', encoding='utf-8')

        # read() 可能会抛出编码错误，或者我们后续处理可能抛出 ValueError
        content = f.read()

        # 模拟业务逻辑：假设我们要求文件内容必须转为整数
        # (如果文件里是文字，这行会抛出 ValueError)
        num = int(content)

    except FileNotFoundError:
        # 2. 捕获特定的错误：文件找不到
        print("❌ 错误捕获：找不到这个文件，请检查路径。")

    except ValueError:
        # 2. 捕获另一种错误：内容格式不对
        print("❌ 错误捕获：文件内容不是数字，无法转换。")

    except Exception as e:
        # 2. 兜底捕获：抓住所有其他未知的错误
        print(f"❌ 未知错误：发生了意料之外的问题 -> {e}")

    else:
        # 3. 只有无错时才执行
        print("✅ 成功执行：文件读取并转换成功！")
        print(f"   读取到的数字是: {num}")

    finally:
        # 4. 无论如何都会执行
        # 这里的任务是：如果文件被打开了，一定要关掉它
        if f:
            f.close()
            print("🔒 资源清理：文件已安全关闭。")
        else:
            print("🔒 资源清理：文件打开失败，无需关闭。")
        print("--- 流程结束 ---\n")


# ==========================================
# 下面我们来制造三种情况进行测试
# ==========================================

# 场景 A: 正常情况 (创建一个包含数字的文件)
with open("success.txt", "w") as temp:
    temp.write("100")
safe_file_reader("success.txt")

# 场景 B: 错误情况 1 - 文件内容不对 (创建一个包含文字的文件)
with open("bad_content.txt", "w") as temp:
    temp.write("Hello World")
safe_file_reader("bad_content.txt")

# 场景 C: 错误情况 2 - 文件根本不存在
safe_file_reader("non_existent_file.txt")

# 清理测试生成的垃圾文件
try:
    os.remove("success.txt")
    os.remove("bad_content.txt")
except:
    pass