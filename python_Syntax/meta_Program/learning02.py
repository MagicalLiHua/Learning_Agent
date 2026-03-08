registry = {}

# 1. 定义一个元类（继承自 type）
class AgentMeta(type):
    # 这个 __new__ 会在带有这个元类的 "普通类" 被创建时自动触发
    def __new__(mcs, name, bases, attrs):
        # 1. 先调用父类方法，把真正的类创建出来（只生一次）
        cls = super().__new__(mcs, name, bases, attrs)

        # 2. 把创建好的类存入注册表
        registry[name] = cls

        # 3. 返回这个类供外部使用
        return cls


class BaseAgent(metaclass=AgentMeta):
    def __getattr__(self, name):
        def func(*args, **kwargs):
            # 这里加入了 self.role 来证明它能读取到动态绑定的属性
            print(f"[{self.role}] 准备将指令发给 LLM: 方法名={name}, 参数={kwargs}")
        return func


# 2. 外部配置
agent_configs = [
    {"name": "CoderAgent", "role": "programmer"},
    {"name": "PMAgent", "role": "product manager"}
]

agent_classes = {}

# 3. 你的任务：写 for 循环生成类，存入 agent_classes
for agent in agent_configs:
    agent_classes[agent["name"]] = type(agent["name"], (BaseAgent,), {"role": agent["role"]})

print(registry)  # 输出注册的类