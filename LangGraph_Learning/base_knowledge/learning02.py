from langgraph.constants import START, END
from langgraph.graph import StateGraph
builder = StateGraph(dict)

def addition(state):
    """
    执行加法运算的节点函数

    参数:
        state (dict): 包含输入数据的状态字典，必须包含键"x"

    返回:
        dict: 返回更新后的状态字典，其中"x"的值增加1
    """
    print(f'加法节点收到的初始值:{state}')
    return {"x": state["x"] + 1}

def subtraction(state):
    """
    执行减法运算的节点函数

    参数:
        state (dict): 包含输入数据的状态字典，必须包含键"x"

    返回:
        dict: 返回更新后的状态字典，其中"x"的值减少2
    """
    print(f'减法节点收到的初始值:{state}')
    return {"x": state["x"] - 2}

# 向图构建器中添加节点
# 添加加法运算节点和减法运算节点到构建器中
builder.add_node("addition", addition)
builder.add_node("subtraction", subtraction)

# 定义节点之间的执行顺序 edges
# 设置节点间的依赖关系，形成执行流程图
builder.add_edge(START, "addition")
builder.add_edge("addition", "subtraction")
builder.add_edge("subtraction", END)
# 编译图构建器生成计算图
graph = builder.compile()

# 打印图的边和节点信息
print(builder.edges)
print(builder.nodes)
# 打印图的可视化结构
print(graph.get_graph().print_ascii())