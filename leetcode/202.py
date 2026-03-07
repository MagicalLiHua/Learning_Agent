class Solution:
    def isHappy(self, n: int) -> bool:
        sum = 0
        record = {}

        while n != 1:
            while n > 0:
                curr = n % 10
                sum = sum + curr*curr
                n = n // 10
                # print(sum)
            if sum not in record:
                record[sum] = 1
                n = sum
                sum = 0
            else:
                return False

        return True

s = Solution()
# s.isHappy(19)
print(s.isHappy(19))