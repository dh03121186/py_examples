import os
import sys
import re

# 映射表
c_a = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000,
    '零': 0,
    '两': 2,
}

next_unit = {
    '百': '十',
    '千': '百',
    '万': '千',
    '亿': '千万',
}


def input_standard(c_num):
    # 一万三--一万三千，三亿二--三亿两千万，三千万三？， 三千亿四？，暂时以最后一个数字的前一个单一单位（万/亿/千/百）为基准计算最后一位数字的单位
    if re.search(r'[亿万千百][一二三四五六七八九]$', c_num):
        c_num += next_unit.get(c_num[-2])

    num_list = c_num.split('亿')
    for i in range(len(num_list)):
        num_list[i] = num_list[i].strip('零')
    standard_num = '亿'.join(num_list)
    num_list = standard_num.split('万')
    for i in range(len(num_list)):
        num_list[i] = num_list[i].strip('零')
    # 将输入的数字规范化：两-->二，如果十前面的数字是零或者没有（中文习惯会省去，比如一十二会说成十二）则添加一
    standard_list = standard_num.split('十')

    for i in range(len(standard_list)):
        if standard_list[i].endswith('零') or standard_list[i] == '':
            standard_list[i] += '一'
    # 如果是以十结尾会出现十后面多一个一的bug，去掉最后一个
    if standard_num.endswith('十'):
        standard_list[-1] = ''
    return_num = '十'.join(standard_list)
    # 如果以单位开始，在单位前添加一
    if re.match(r'[亿万千百十]', return_num):
        return_num = '一' + return_num
    return return_num


def base_calculate(c_num):
    """除开单位的基本数字计算: 五百三十一"""
    # 单位顺序由大到小
    unit_list = re.findall(r'[十百千]', c_num)
    for i in range(len(unit_list) - 1):
        if c_a.get(unit_list[i]) <= c_a.get(unit_list[i+1]):
            return False

    if not c_num:
        return 0
    num_list = [c_a.get(c) for c in c_num]
    num_sum = 0
    for i in range(len(num_list)):
        # 单位判断
        if num_list[i] > 0 and num_list[i] % 10 == 0:
            num_sum += num_list[i] * num_list[i-1]
    if num_list[-1] < 10:
        num_sum += num_list[-1]

    return num_sum


def illegal_input_verification(c_num):
    """输入的合法性校验"""
    # 1. 是否存在非数字的字符
    legal_chars = set(c_a.keys())
    input_chars = set(list(c_num))
    if len(input_chars - legal_chars) > 0:
        return False
    # 2. 单位相连且小的单位在后: 万十
    counting_unit_list = re.findall(r'[亿万千百十]+', c_num)
    for counting_unit in counting_unit_list:
        # 百十这种的不合法，万万也不合法
        if re.search(r'[十百千]{2}', counting_unit) or re.search(r'万万', counting_unit):
            return False
        # 过了第一层筛选，再判断小的单位是否在大的单位后
        for i in range(len(counting_unit) - 1):
            if c_a.get(counting_unit[i]) > c_a.get(counting_unit[i+1]):
                return False
    # 3. 万个数不能超过两个，是两个的时候需要校验第一个万是否是万亿，不然就不合法
    if c_num.count("万") == 2:
        if c_num[c_num.index('万') + 1] != '亿':
            return False
    elif c_num.count('万') > 2:
        return False

    return True


def c_num_2_num(c_num):

    def calculate_billion_left(left_num):
        """计算亿左边的数字"""
        try:
            index_of_billion = left_num.rindex('亿')
        except ValueError:  # 捕捉异常说明不存在亿了，然后按照万计算
            if '万' in left_num:
                return (calculate_ten_thousand_left(left_num)) * c_a.get("亿")
            else:
                return (calculate_ten_thousand_right(left_num)) * c_a.get("亿")
        else:
            right_num = '零' if left_num.endswith('亿') else left_num[index_of_billion + 1:]
            return calculate_billion_left(left_num[:index_of_billion]) +\
                   calculate_billion_right(right_num)

    def calculate_billion_right(right_num):
        """计算亿右边的数字"""
        try:
            index_of_billion = right_num.rindex('亿')
        except ValueError:  # 捕捉异常说明不存在亿了，然后按照万计算
            if '万' in right_num:
                return calculate_ten_thousand_left(right_num)
            else:
                return calculate_ten_thousand_right(right_num)
            # return calculate_ten_thousand_left(right_num)
        else:
            right_num = '零' if right_num.endswith('亿') else right_num[index_of_billion + 1:]
            return calculate_billion_left(right_num[:index_of_billion]) +\
                   calculate_billion_right(right_num)

    def calculate_ten_thousand_left(left_num):
        """计算万左边的数字"""
        try:
            index_of_ten_thousand = left_num.rindex('万')
        except ValueError:  # 捕捉异常说明不存在万了，就能直接计算
            return_num = base_calculate(left_num)
            if return_num is False:
                raise ValueError
            else:
                return return_num * c_a.get("万")
        else:  # 没有异常说明仍存在万，递归计算
            right_num = '零' if left_num.endswith('万') else left_num[index_of_ten_thousand+1:]
            return calculate_ten_thousand_left(left_num[:index_of_ten_thousand]) +\
                   calculate_ten_thousand_right(right_num)

    def calculate_ten_thousand_right(right_num):
        """计算万右边的数字"""
        try:
            index_of_ten_thousand = right_num.rindex('万')
        except ValueError:  # 捕捉异常说明不存在万了，就能直接计算
            return_num = base_calculate(right_num)
            if return_num is False:
                raise ValueError
            else:
                return return_num
        else:  # 没有异常说明仍存在万，递归计算
            right_num = '零' if right_num.endswith('万') else right_num[index_of_ten_thousand+1:]
            return calculate_ten_thousand_left(right_num[:index_of_ten_thousand]) +\
                   calculate_ten_thousand_right(right_num)

    # 1. 输入规范化
    c_num = input_standard(c_num)

    # 2. 合法校验
    if not illegal_input_verification(c_num):

        return '输入不合法，请重新输入'
    
    # 万和亿是中文数字的两个节点单位, 亿是最大的中文计量单位，如果是亿亿的话就得做额外处理
    # 3. 计算
    if '亿' in c_num:
        return calculate_billion_left(c_num)
    else:
        return calculate_billion_right(c_num)


if __name__ == '__main__':
    """中文数字装阿拉伯数字"""

    input_c_num = input("请输入需要转换的中文数字:")
    while input_c_num != 'q':
        try:
            print(c_num_2_num(input_c_num))
        except:
            print('输入数字不合法:{}'.format(input_c_num))
        input_c_num = input("请输入需要转换的中文数字:")

    print('谢谢访问')