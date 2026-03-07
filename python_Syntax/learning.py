# a = [1, 2, 3, 4]  # 变量 a 是一个新的列表, [1, 2, 3, 4]
# b = a             # 变量 b 赋值了变量 a 的值
# print(b is a)            # => True, a 和 b 引用的是同一个对象
# print(b == a)             # => True, a 和 b 的对象的值相同
# b = [1, 2, 3, 4]  # 变量 b 赋值了一个新的列表, [1, 2, 3, 4]
# print(b is a)            # => False, a 和 b 引用的是不同的对象
# print(b == a)             # => True, a 和 b 的对象的值相同

filled_dict = {"one": 1, "two": 2, "three": 3}

print(list(filled_dict.keys()))

print(list(filled_dict.values()))

print("two" in filled_dict)

print(filled_dict.get("two"))

print(filled_dict.get("four",None))  # None

# []  # 空列表
# ()  # 空元组
# {}  # 空字典
# {}  # 空集合（错误的写法，实际上这是一个空字典）
# {}  当不存在键值对的时候，花括号表示一个空字典，而不是一个空集合。
# {1, 2, 3}  花括号表示一个集合，包含元素 1、2 和 3。

# 用 set 表达集合
# empty_set = set()
# 初始化一个集合，语法跟字典相似。
some_set = {1, 1, 2, 2, 3, 4}   # some_set现在是 {1, 2, 3, 4}

print(some_set)  # 输出: {1, 2, 3, 4}，重复的元素被自动去除

