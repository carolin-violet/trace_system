"""
配置文件
"""

class Config(object):
    """项目的配置"""
    DEBUG = True
    SECRET_KEY = 'J5RxXy9emBt78iIVP1beu4k4XbbgWxcZI+UrvD7afM9tXNPmnHw8xn4c5+qjnEB1'
    # 为Mysql添加配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zj20001125@127.0.0.1:3306/trace_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 修改数据模型后自动执行，不需要commit()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # # Redis的配置
    # REDIS_HOST = '127.0.0.1'
    # REIDS_PORT = 6379
    #
    # # Session保存配置
    # SESSION_TYPE = 'redis'
    # # 开启session签名
    # SESSION_USE_SIGNER = True
    # # 指定Session保存的redis
    # SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REIDS_PORT)
    # # 设置需要过期
    # SESSION_PERMANENT = False
    # # 设置过期时间
    # PERMANENT_SESSION_LIFETIME = 86400 * 2
    # # 设置日志等级
    # LOG_LEVEL = logging.DEBUG
