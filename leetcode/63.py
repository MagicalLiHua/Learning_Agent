from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [0] * len(obstacleGrid[0])

        for i in range(0, len(dp)):
            if obstacleGrid[0][i] == 1:
                while i < len(dp):
                    dp[i] = 0
                    i += 1
                break
            else:
                dp[i] = 1

            # print(i)
            # print(f"dp[{i}] = {dp[i]}")

        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0
                else:
                    dp[j] = dp[j] + dp[j - 1]

                print(f"dp[{j}] = {dp[j]}")

        print(dp)

        return dp[-1]


sol = Solution()
# print(sol.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]))  # 输出: 2
print(sol.uniquePathsWithObstacles([[1,0]]))  # 输出: 0