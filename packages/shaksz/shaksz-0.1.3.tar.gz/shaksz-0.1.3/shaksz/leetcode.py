'''
LeetCode Problem 1: Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
'''
def twoSum(nums, target):
      hash_map = {}
      for i, num in enumerate(nums):
          difference = target - num
          if difference in hash_map:
            return [hash_map[difference], i]
          hash_map[num] = i
      return []

'''
LeetCode Problem 1550. Three Consecutive Odds
Given an integer array arr, return true if there are three consecutive odd numbers in the array. Otherwise, return false.
'''
def threeConsecutiveOdds(arr):
    """
    :type arr: List[int]
    :rtype: bool
    """
    size = len(arr)                                                         # Get the size of the array
    if size <=2:                                                            # If size is less than or equal to 2, return False
        return False                                                        # Since it's impossible to have three consecutive odds
    for i in range(size - 2):                                               # Iterate through the array
        if arr[i] % 2 != 0 and arr[i+1] % 2 != 0 and arr[i+2] % 2 != 0:     # Check if three consecutive numbers are odd
            return True                                                     # If found, return True
    return False                                                            # If no such triplet is found, return False