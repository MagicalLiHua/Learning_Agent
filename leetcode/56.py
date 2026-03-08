C, N = map(int, input().split())

# 2. 分别读取下面三行，并转为整数列表
# 每行都有 N 个数字，直接转成 list
weights = list(map(int, input().split())) # 矿石重量 w[i]
values = list(map(int, input().split()))  # 矿石价值 v[i]
counts = list(map(int, input().split()))  # 矿石数量 k[i]

w_n = []
v_n = []

for i in range(len(counts)):
    for j in range(counts[i]):
        w_n.append(weights[i])
        v_n.append(values[i])

dp = [0] * (C+1)

for i in range(1,C+1):
    for j in range(len(w_n)-1,0,-1):
        if w_n[j] > i:
            continue
        else:
            dp[i] = max(dp[i],dp[i-w_n[j]]+v_n[j])

print(dp[-1])