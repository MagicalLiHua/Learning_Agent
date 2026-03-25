import torch

# # 创建一个1维张量 (向量)
# v = torch.tensor([1.0, 2.0, 3.0])
# print("向量 v:\n", v)
# print("v 的维度 (shape):", v.shape)
#
# # 创建一个2维张量 (矩阵)
# M = torch.tensor([[1.0, 2.0],
#                   [3.0, 4.0]])
# print("矩阵 M:\n", M)
# print("M 的维度 (shape):", M.shape)
#
# M = torch.tensor([[1.0, 0.0,0.0],
#                   [0.0, 1.0,0.0],
#                   [0.0, 0.0, 1.0]])

# M = torch.eye(3)
#
# print("M:\n", M)

W = torch.tensor([[2.0, 1.0],
                  [0.0, 3.0]])

x = torch.tensor([[1.0],
                  [2.0]])

y = W @ x
y = W.matmul(x)
print(y)