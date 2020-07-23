from typing import List
"""
在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，
但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

"""


def find_repeat_num(nums: List[int]):
    """
    思路: 初始化一个长度为n，并且都为0的数组A，输入的数组B里面每一个元素的值都对应A的index，并且将该处的值+1
    如果某个位置的元素不为1，这个就重复了
    :param nums:
    :return:
    """
    a = [0 for i in range(len(nums))]
    for num in nums:
        if a[num] == 0:
            a[num] = 1
        else:
            return num
    return None


if __name__ == '__main__':
    test_list = [4, 5, 5, 1, 0, 3]
    result = find_repeat_num(test_list)
    if result:
        print(result)
    else:
        print("不存在重复元素")
