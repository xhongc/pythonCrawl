# class Solution:
#     def twoSum(self, nums, target):
#
#         for each in range(target+1):
#
#             if each in nums and (target-each) in nums :
#                 i = nums.index(each)
#                 try:
#                     k = nums.index(target-each,i+1,len(nums))
#                     return [i, k]
#                 except:
#                     k = nums.index(target-each,0,i+1)
#                     return [k,i]
#
#
# A = Solution()
# print(A.twoSum([-3,2,3,4],0))

# class Solution:
#     def twoSum(self, nums, target):
#
#         for one in nums:
#             i = nums.index(one)
#             for two in nums[i+1:]:
#                 try:
#                     j = nums.index(two,i+1,len(nums))
#                 except:
#                     j = nums.index(two,0,i+1)
#
#                 if i !=j:
#                     if one+two ==target or two+one ==target:
#                         return [i,j]


class Solution:
    def twoSum(self, nums, target):
        nums_hash = {}
        for i in range(len(nums)):
            if target - nums[i] in nums_hash:
                return [nums_hash[target - nums[i]], i]
            nums_hash[nums[i]] = i

A = Solution()
print(A.twoSum([3,0,3],6))
