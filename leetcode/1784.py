class Solution:
    def checkOnesSegment(self, s: str) -> bool:
        left, right = 0, 0
        count = 0

        while left < len(s):
            if s[left] == "1":
                count += 1
                right = left + 1
                while right < len(s) and s[right] == "1":
                    right += 1
                left = right
            else:
                left += 1

        if count == 0 or count == 1:
            return True

        return False


sol = Solution()

sol.checkOnesSegment("1001")