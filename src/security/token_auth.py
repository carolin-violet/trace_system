from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from src.settings import Config

'''
生成token
'''


def create_token(user_id):
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(Config.SECRET_KEY, Config.TOKEN_EXPIRATION)
    # 接收用户id转换与编码
    token = s.dumps({"user_id": user_id}).decode("ascii")
    return token


'''
验证token
'''


def verify_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
        try:
            return data
        except Exception:
            return '用户不存在'
    except Exception:
        return 'token过期或错误'






