from typing import List


class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        if len(nums) < 4:
            return False
        slow, fast = 0, 1
        # while nums[slow] < nums[fast] and fast < len(nums):
        while fast < len(nums) and nums[slow] < nums[fast]:
            slow += 1
            fast += 1
        if nums[slow] == nums[fast]:
            return False
        while fast < len(nums) and nums[slow] > nums[fast]:
            slow = fast
            fast += 1
        if nums[slow] == nums[fast]:
            return False
        while fast < len(nums) and nums[slow] < nums[fast]:
            slow = fast
            fast += 1
        if fast == len(nums):
            return True
        else:
            return False

c = Solution()
print(c.isTrionic([1, 3, 1, 4]))