class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        result = []
        while x > 0:
            result.append(x % 10)
            x = int(x / 10)
        left, right = 0, len(result) - 1
        while left != right:
            if result[left] != result[right]:
                return False
            left += 1
            right -= 1
        return True

s = Solution()
print(s.isPalindrome(11))  # True