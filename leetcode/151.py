class Solution:
    def reverseWords(self, s: str) -> str:
        result = []
        strResult = ""

        ListS = list(s)
        j = 0

        while j < len(ListS):
            currWord = ""

            while j <len(ListS) and ListS[j] != " ":
                currWord += ListS[j]
                j+=1
            if currWord != "":
                result.append(currWord)
            j+=1

        index = len(result) - 1

        while index > 0:
            strResult += result[index]
            strResult += " "
            index -= 1

        strResult += result[index]
        return strResult


sol = Solution()

print(sol.reverseWords("  hello world  "))