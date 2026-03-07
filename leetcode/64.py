from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        dp = [[0] * n for _ in range(m)]
        dp[0][0] = grid[0][0]

        for i in range(1, n):
            dp[0][i] = grid[0][i] + grid[0][i - 1]

        for j in range(1, m):
            dp[j][0] = grid[j][0] + grid[j - 1][0]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j] + grid[i][j], dp[i][j - 1] + grid[i][j])

        print(dp)

        return dp[m - 1][n - 1]

sol = Solution()
grid = [
    [1,3,1],
    [1,5,1],
    [4,2,1]
]
print(sol.minPathSum(grid))