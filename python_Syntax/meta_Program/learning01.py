class BaseAgent:
    def __getattr__(self, name):
        def func(*args, **kwargs):
            print(f"Function {name} is called with args: {args} and kwargs: {kwargs}")
        return func


agent_configs = [
    {"name": "CoderAgent", "role": "programmer", "job": "write code"},
    {"name": "PMAgent", "role": "product manager", "job": "design products"}
]

agent_list = {}

for agent in agent_configs:
    agent_list[agent["name"]] = type(agent["name"],(BaseAgent,),{"role":agent["role"],"job":agent["job"]})

coder = agent_list["CoderAgent"]()
print(coder.analyze_data())