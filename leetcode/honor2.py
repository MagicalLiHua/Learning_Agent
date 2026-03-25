import sys


def solve():
    valid_set = set()  # 用于合法字符串去重
    valid_list = []  # 用于存储去重后的合法字符串
    invalid_list = []  # 用于存储所有非法字符串

    # 定义合法字符判断函数
    def is_valid(s):
        if not s: return False
        for char in s:
            if not (('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9')):
                return False
        return True

    # 定义循环左移函数
    def left_rotate(s, n):
        if not s: return s
        n = n % len(s)  # 防止移动位数超过字符串长度
        return s[n:] + s[:n]

    # --- 1. 读取输入 ---
    # 题目要求以空行结束，sys.stdin 会持续读取直到 EOF 或手动判断空行
    lines = sys.stdin.readlines()

    for line in lines:
        word = line.strip()
        if not word:
            break

        if is_valid(word):
            if word not in valid_set:
                valid_set.add(word)
                valid_list.append(word)
        else:
            invalid_list.append(word)

    # --- 2. 处理合法字符串 ---
    # 步骤：循环左移 10 次 -> 排序
    processed_valid = []
    for s in valid_list:
        rotated = left_rotate(s, 10)
        processed_valid.append(rotated)

    # 按 ASCII 排序
    sorted_processed =  sorted(processed_valid)

    print(" ".join(valid_list))

    print(" ".join(invalid_list))

    print(" ".join(processed_valid))

    print(" ".join(sorted_processed))


if __name__ == "__main__":
    solve()