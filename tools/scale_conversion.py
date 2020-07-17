# coding=UTF-8
# scale_conversion.py

"""
- id 压缩方案, 用于生成标签暗码
    - 把 id 转成 36进制
    - 4位可用 36 ** 4 = 1,679,616 情况
- 提供 36 转 10进制 func
"""


def base10toN(num, n=36):
    """
        十进制 -> N进制
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    current = num
    while current != 0:
        res = chars[current % n] + res
        current = current / n
    return res


def baseNto10(s, n=36):
    """
        N进制 -> 十进制
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    depth = res = 0
    for char in s[::-1]:
        res += chars.index(char) * (n ** depth)
        depth += 1
    return res


if __name__ == '__main__':

    J = 36
    number = 678123

    num_char = base10toN(number, J)
    new_num = baseNto10(num_char, J)

    print("origin number", number)
    print("number char", num_char)
    print("number after converse", new_num)


