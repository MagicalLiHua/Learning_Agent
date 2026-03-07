class Solution:
    def numTrees(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[1] = 1

        for i in range(2, len(dp)):
            for j in range(1, i + 1):
                dp[i] += dp[j] * dp[i - j]

        print(dp)

        return dp[-1]

sol = Solution()
print(sol.numTrees(3))
print(sol.numTrees(4))