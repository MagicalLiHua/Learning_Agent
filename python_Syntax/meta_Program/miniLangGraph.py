from typing import Annotated, TypedDict, get_type_hints
import operator


# ==========================================
# 1. 定义你的状态结构 (Schema)
# ==========================================
class AgentState(TypedDict):
    # 普通类型：直接覆盖新值
    step_count: int
    # Annotated 类型：用附加的函数(operator.add)合并新旧值
    messages: Annotated[list, operator.add]


# ==========================================
# 2. 框架底层的状态更新引擎
# ==========================================
def update_state(current_state: dict, new_data: dict, state_schema: type) -> dict:
    """
    根据 schema (类型声明) 智能更新当前状态。
    """
    # 拿到所有的类型提示，include_extras=True 保证能拿到 Annotated 里的 metadata
    hints = get_type_hints(state_schema, include_extras=True)

    # 复制一份当前状态
    updated_state = current_state.copy()

    for key, new_value in new_data.items():
        if key not in hints:
            continue

        hint = hints[key]

        # TODO: 你的任务在这里！
        # 1. 判断 hint 是否具有 "__metadata__" 属性 (可用 hasattr 检查)
        # 2. 如果有，提取出里面的操作函数 (它是一个元组，通常取第 0 个元素)
        # 3. 如果当前状态 (updated_state) 已经有这个 key，并且提取到了操作函数，
        #    就用这个函数把 旧值 和 new_value 合并，存回 updated_state[key]
        # 4. 如果没有 __metadata__ 或者 是第一次赋值，就直接让 updated_state[key] = new_value

        if hasattr(hint, "__metadata__"):
            reducer_func = hint.__metadata__[0]
            if key in updated_state:
                updated_state[key] = reducer_func(updated_state[key], new_value)
            else:
                updated_state[key] = new_value
        else:
            updated_state[key] = new_value

    return updated_state


# ==========================================
# 3. 运行测试
# ==========================================
if __name__ == "__main__":
    # 假设这是当前的对话状态
    current_state = {
        "step_count": 1,
        "messages": ["User: 你好"]
    }

    # 这是 Agent 刚刚产生的新状态
    new_data = {
        "step_count": 2,  # 步骤更新为 2
        "messages": ["Agent: 你好！我是AI助手"]  # 新产生的一条消息
    }

    # 执行状态引擎更新
    final_state = update_state(current_state, new_data, AgentState)

    print("更新前的状态:", current_state)
    print("更新后的状态:", final_state)

    # 期望的完美输出应该是：
    # 更新后的状态: {'step_count': 2, 'messages': ['User: 你好', 'Agent: 你好！我是AI助手']}