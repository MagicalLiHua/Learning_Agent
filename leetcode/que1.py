from collections import deque
from typing import List


class Solution:
    def countStudents(self, students: List[int], sandwiches: List[int]) -> int:
        n = len(students)
        queStuents = deque(students)
        queSandwichs = deque(sandwiches)

        count = 0
        while count < n * n:
            if not queStuents:
                break
            if queStuents[0] == queSandwichs[0]:
                queSandwichs.popleft()
                queStuents.popleft()
            else:
                temp = queStuents.popleft()
                queStuents.append(temp)

            count += 1

        return len(queStuents)


students = [0,0,0,1,1,1,1,0,0,0]
sandwiches = [1,0,1,0,0,1,1,0,0,0]

sol = Solution()
result = sol.countStudents(students, sandwiches)
print(result)  # 输出结果