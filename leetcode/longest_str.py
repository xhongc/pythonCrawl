class Solution(object):
    def lengthOfLongestSubstring(self, s):
        dict1 = {}
        count = 0
        maxlen = 0
        for i in range(len(s)):
            if s[i] in dict1 and count <= dict1[s[i]]:
                count = dict1[s[i]] +1
            else:
                maxlen = max(maxlen,i-count+1)
            dict1[s[i]] = i
        return maxlen
a = Solution()
print(a.lengthOfLongestSubstring('abcabcbb'))

