class Solution(object):
    def __init__(self):
        self.res = []

    def validSequence(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: List[int]
        """

        dp = [-1]*len(word2)
        j = len(word2)-1
        for i in range(len(word1)-1, -1, -1):
            if word1[i] == word2[j]:
                dp[j] = i
                j-=1
            if j < 0:
                break
        
        j = 0
        ans = []
        flag = True
        for i in range(len(word1)):
            if word1[i] == word2[j] or (flag and(j == len(word2)-1 or i+1 <= dp[j+1])):
                if word1[i] != word2[j]:
                    flag = False
                
                j+=1
                ans.append(i)
            
            if j >= len(word2):
                break
        
        if len(ans) == len(word2):
            return ans
        ans = []
        return ans

                