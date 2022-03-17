from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from src.settings import Config
import functools
from flask import request


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return '缺少参数token'

        s = Serializer(Config.SECRET_KEY)
        try:
            s.loads(token)
        except Exception:
            return "登录已过期"

        return view_func(*args, **kwargs)

    return verify_token
'''
生成token
'''


def create_token(user_id):
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(Config.SECRET_KEY, Config.TOKEN_EXPIRATION)
    # 接收用户id转换与编码
    token = s.dumps({"id": user_id}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(Config.SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    print(data)
    return True
