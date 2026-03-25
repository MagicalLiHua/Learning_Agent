import sys


def main():
    # 1. 读取所有输入数据
    input_data = sys.stdin.read().strip()
    if not input_data:
        return

    # 按分号分割每个 include 关系
    pairs = input_data.split(';')

    graph = {}
    root = None

    # 2. 构建有向图（邻接表）
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        # 按空格分割出包含者和被包含者
        parts = pair.split()
        if len(parts) == 2:
            u, v = parts[0], parts[1]
            # 题目保证所有关系都由第一个头文件直接或间接引入，所以第一对的 u 就是根节点
            if root is None:
                root = u

            # 初始化字典列表
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []

            # 添加有向边 u -> v
            graph[u].append(v)

    # 3. 深度优先搜索 (DFS) 与状态记录
    expand_list = []  # 用于记录展开顺序 (EXPAND)
    expanded_set = set()  # 用于 O(1) 快速判断是否已经被彻底展开过
    path = []  # 用于记录当前的 DFS 递归路径，寻找环
    cycles = []  # 用于记录找到的环 (CIRCLE)

    def dfs(node):
        # 前序遍历：第一次遇到该节点时记录
        expand_list.append(node)
        expanded_set.add(node)
        path.append(node)

        # 遍历该节点依赖的所有头文件
        for neighbor in graph.get(node, []):
            if neighbor in path:
                # 核心：如果依赖的节点已经在当前访问路径中，说明检测到了环！
                # 截取从环起点到当前节点再回到起点的路径
                idx = path.index(neighbor)
                cycle_path = path[idx:] + [neighbor]
                cycles.append(" ".join(cycle_path))
            elif neighbor not in expanded_set:
                # 如果没有成环，且该节点之前从未被展开过，则继续 DFS 深入
                dfs(neighbor)
            # 如果 neighbor 既不在 path 里，也在 expanded_set 里，
            # 说明是从别的分支已经展开过的头文件，不需要重复处理

        # 该节点的所有依赖处理完毕，从当前路径中回溯弹出
        path.pop()

    # 从根节点开始模拟展开
    if root is not None:
        dfs(root)

    # 4. 按照题目要求的格式输出结果
    print(f"EXPAND:{' '.join(expand_list)}")

    if not cycles:
        # 没有检测到任何环
        print("CIRCLE:")
    else:
        # 有一个或多个环，按分号拼接
        print(f"CIRCLE:{';'.join(cycles)}")


if __name__ == "__main__":
    main()