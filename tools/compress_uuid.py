# -*- coding: utf-8 -*-

import uuid

SAFEHASH = [x for x in "0123456789-abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def compress_uuid():
    """
        根据http://www.ietf.org/rfc/rfc1738.txt,由uuid编码扩大字符域生成串
        包括: [0-9a-zA-Z\-_] 共64个
        长度: (32-2)/3*2 = 20
        备注: 可在地球上人人都用,使用100年不重复(2^120)
        :return: str
    """

    row = str(uuid.uuid4()).replace('-', '')
    safe_code = ''
    for i in xrange(10):
        enbin = "%012d" % int(bin(int(row[i * 3] + row[i * 3 + 1] + row[i * 3 + 2], 16))[2:], 10)
        safe_code += (SAFEHASH[int(enbin[0:6], 2)] + SAFEHASH[int(enbin[6:12], 2)])
    return safe_code
