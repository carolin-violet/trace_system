import rsa
from base64 import b64encode, b64decode
import pickle
import json

'''
生成公私钥对,
512这个数字表示可以加密的字符串长度，可以是1024，4096等等，
由于生成的公私钥对是对象，所以需要用pickle先将对象序列化成二进制字节,再用base64编码压缩一下二进制字节存入数据库
'''


def create_keys():
    public_key, private_key = rsa.newkeys(512)
    return b64encode(pickle.dumps(public_key)), b64encode(pickle.dumps(private_key))


'''
从数据库中读取的密钥二进制字节需要转换为密钥对象
'''


def normalize_keys(key):
    return pickle.loads(b64decode(key))


'''
对明文用公钥加密,得到二进制类型的密文
'''


def encrypt(message, public_key):
    default_length = 53  # 每次最多加密53字节
    if type(message) == dict:
        message = json.dumps(message, sort_keys=True)

    '''
    当需加密的数据超过53字节时就分段加密
    '''
    if len(message.encode('utf-8')) > 53:
        message_list = make_group(message.encode('utf-8'), default_length)
        cipher = json.dumps([str(rsa.encrypt(i, normalize_keys(public_key))) for i in message_list])
    else:
        cipher = str(rsa.encrypt(message.encode('utf-8'), normalize_keys(public_key)))
    return cipher


'''
对密文用私钥解密获得明文
'''


def decrypt(cipher, private_key):
    message = rsa.decrypt(cipher, normalize_keys(private_key)).decode('utf-8')
    return message


'''
进行数字签名,获得二进制的签名
'''


def get_signature(message, private_key):
    return rsa.sign(message, normalize_keys(private_key), 'SHA-256')


'''
验证签名,res正常就返回true,出现rsa.pkcs1.VerificationError错误就返回error
'''


def verify_signature(message, signature, public_key):
    res = rsa.verify(message, signature, normalize_keys(public_key))
    try:
        if res:
            return 'true'
    except rsa.pkcs1.VerificationError:
        return 'error'


'''
对长数据进行分组
'''


def make_group(data, default_length):
    final_data = []
    i = 0
    while True:
        if (i + default_length) > len(data):
            final_data.append(data[i:])
            break
        final_data.append(data[i:i+default_length])
        i += default_length
    return final_data




# if __name__ == '__main__':
#     pub_key, pri_key = create_keys()
#
#     qqqq = {
#         "a": 'faw'
#     }
#     cipher_text = encrypt(qqqq, pub_key)
#     print(cipher_text)
#     mes = decrypt(cipher_text, pri_key)
#     print(mes)
