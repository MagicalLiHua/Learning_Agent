from typing import Annotated, get_type_hints
import operator

class MockState:
    messages: Annotated[list, operator.add]

# include_extras=True 的意思是：不要只拿 list，把 Annotated 里的附加物也一并拿出来
hints = get_type_hints(MockState, include_extras=True)

# 打印看看我们抓到了什么
print(hints['messages'])

reducer_func = hints['messages'].__metadata__[0]  # 从 Annotated 的元数据里拿到 operator.add
print(reducer_func)  # 输出 <built-in function add>
old_data ="Hello, "
new_data = "world!"
result = reducer_func(old_data, new_data)  # 用 operator.add 来合并字符串
print(result)  # 输出 "Hello, world!"