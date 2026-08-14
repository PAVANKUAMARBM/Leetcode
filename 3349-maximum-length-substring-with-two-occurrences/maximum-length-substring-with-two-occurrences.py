class Solution:
    def maximumLengthSubstring(self, s):
        n = len(s)
        maxLen = 0
        for i in range(n):
            arr = [0] * 26
            for j in range(i, n):
                arr[ord(s[j]) - ord('a')] += 1
                if arr[ord(s[j]) - ord('a')] == 3:
                    break
                maxLen = max(maxLen, j - i + 1)
        return maxLen