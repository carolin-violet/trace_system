"""
配置文件
"""


class Config(object):
    """项目的配置"""
    DEBUG = True
    SECRET_KEY = 'J5RxXy9emBt78iIVP1beu4k4XbbgWxcZI+UrvD7afM9tXNPmnHw8xn4c5+qjnEB1'
    # 为Mysql添加配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zj20001125@127.0.0.1:3306/trace_system'

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 修改数据模型后自动执行，不需要commit()
    SQLALCHEMY_POOL_SIZE = 5  # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）
    SQLALCHEMY_POOL_TIMEOUT = 10  # 指定数据库连接池的超时时间。默认是 10
    # 自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时
    SQLALCHEMY_POOL_RECYCLE = 1

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
