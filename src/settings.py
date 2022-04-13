"""
配置文件
"""


class Config(object):
    """项目的配置"""

    ENV = "development"  # 生态环境        development：开发者模式   production： 生产模式
    DEBUG = True

    SECRET_KEY = 'J5RxXy9emBt78iIVP1beu4k4XbbgWxcZI+UrvD7afM9tXNPmnHw8xn4c5+qjnEB1'
    TOKEN_EXPIRATION = 36000

    # 为Mysql添加配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zj20001125@127.0.0.1:3306/trace_system'

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 修改数据模型后自动执行，不需要commit()
    SQLALCHEMY_POOL_SIZE = 100  # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）
    SQLALCHEMY_POOL_TIMEOUT = 10  # 指定数据库连接池的超时时间。默认是 10
    # 自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时
    SQLALCHEMY_POOL_RECYCLE = 3600

