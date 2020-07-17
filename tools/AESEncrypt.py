# coding=utf-8

# 这里使用pycrypto‎库
# easy_install pycrypto‎

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

fchr = '\0'  # fill character

"""
AES(Advanced Encryption Standard)对称加密:

对称加密就是公钥和撕咬是

1. 秘钥必须长度是16,24,32
2. 加密之前需要把文本改成16的倍数, 所以需要填充特殊字符
"""


class AEScrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def _fill_text(self, text):
        """
        补位:
            如果text不足16位就用空格补足为16位，
            如果大于16当时不是16的倍数，那就补足为16的倍数。
        """
        length = 16
        count = len(text)
        if count < length:
            add = length - count
            text = text + (fchr * add)
        elif count > length:
            add = (length - (count % length))
            text = text + (fchr * add)
        return text

    def encrypt(self, text):
        """
        加密:
            # 这里密钥key 长度必须为16,24,32
            # 16 (AES-128)
            # 24 (AES-192)
            # 32 (AES-256)
            # 目前AES-128 足够目前使用
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        text = self._fill_text(text)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        """
        解密:
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(fchr)  # 去掉补足的空格用strip()去掉


if __name__ == '__main__':
    obj = AEScrypt('1234567890123456')  # 初始化密钥
    content = u"hesaimaterialasync2020"

    # 加密
    e = obj.encrypt(content)

    # 解密
    d = obj.decrypt(e)
    print("加密:", e)
    print("解密:", d)
