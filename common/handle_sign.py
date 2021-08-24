import base64
import rsa
from time import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto import Random


class HandleSign:
    server_pub = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """

    @classmethod
    def encrypt(cls, msg):
        """
        非对称加密
        :param msg:待加密字符串或者字节
        :return:密文
        """
        msg = msg.encode('utf-8')
        pub_key = cls.server_pub.encode("utf-8")
        public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  # 创建PublicKey对象
        cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
        cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
        return cipher_base64.decode()  # 将字节类型 base64 编码转化为字符串类型

    @classmethod
    def generate_sign(cls, token):
        """
        生成sign
        :param token:token 为str类型
        :param timestamp:当前秒级时间戳，为int类型
        :return:时间戳利sign组成的字典
        """
        timestamp = int(time())  # 获取当前的时间酸
        prefix_50_token = token[:50]  # 获取token 前50位
        message = prefix_50_token + str(timestamp)  # 将token前50位与时间微字符串进行排按
        sign = cls.encrypt(message)  # 生成sign
        return {"timestamp": timestamp, "sign": sign}


if __name__ == '__main__':
    token = 'MIGfMAOGCSqGSIb3DQEBAQUAA4GNADCBiQKBEQDQENQujkLfZfc5Tu9Z1LprzedE03F7gs+7bzrgPsM129LX8UoPYvIG8C604CprBQ4FkfnJpnhWu21vUBOWZyLq6sBrtuPor0c42+gLnFfyhJAwdZB6SqwfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGO8D'
    crypto_info = HandleSign.generate_sign(token)
    print(crypto_info)
    s = '1234567'
