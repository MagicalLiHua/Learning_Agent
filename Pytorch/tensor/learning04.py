import torch

W = torch.tensor([[2.0, 1.0],
                  [0.0, 3.0]])

x = torch.tensor([[1.0],
                  [1.0]], requires_grad=True)

y_target = torch.tensor([[10.0],
                         [10.0]])

lr = 1e-2

for i in range(200):
    y = W @ x
    L = ((y - y_target) ** 2).mean()

    print(f"迭代 {i + 1}, 损失 L: {L.item():.4f}, x: {x.data.flatten()}")

    L.backward()

    with torch.no_grad():
        x -= lr * x.grad
        x.grad.zero_()