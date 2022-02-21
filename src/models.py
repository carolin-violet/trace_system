"""
数据库模型
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


'''
用户基本信息表
'''


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False)  # 用户id
    name = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), unique=True)  # 手机号码,用作登录账号
    password = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(6), nullable=False)  # 性别:male/female

    def __init__(self, user_id, name, phone, password, gender):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.password = password
        self.gender = gender

    def __repr__(self):
        return '<User %r>' % self.userName


'''
商品信息表
'''


class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)  # 商品名称
    price = db.Column(db.Float, nullable=False)  # 商品单价(元/斤)
    weight = db.Column(db.Float, nullable=True)  # 商品重量(斤)
    total = db.Column(db.Float, nullable=True)  # 总价
    commodity_id = db.Column(db.String(255), nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    user_id = db.Column(db.String(50), nullable=False)  # 厂家用户id
    block_info = db.Column(db.Text, default='')  # 二维码信息

    def __init__(self, name, price, weight, total, commodity_id, user_id, block_info=''):
        self.name = name
        self.price = price
        self.weight = weight
        self.total = total
        self.commodity_id = commodity_id
        self.user_id = user_id
        self.block_info = block_info

    def __repr__(self):
        return '<Commodity %r>' % self.name


'''
物流信息
'''


class Logistics(db.Model):
    __tablename__ = 'logistics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_id = db.Column(db.String(255), nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    status = db.Column(db.String(10), nullable=False)  # 商品状态  (已发货, 运输中, 已到货, 已签收)
    com = db.Column(db.String(50), nullable=False)  # 操作的公司名
    time = db.Column(db.String(100), nullable=False)  # 操作时间，需要获取当前系统时间
    ini = db.Column(db.String(100), nullable=False)  # 初始地
    des = db.Column(db.String(100), nullable=False)  # 目的地
    cur = db.Column(db.String(100), nullable=False)  # 当前所在地
    person = db.Column(db.String(20), nullable=False)  # 操作人
    tel = db.Column(db.String(11), nullable=False)  # 操作人联系方式

    def __init__(self, commodity_id, status, com, time, ini, des, cur, person, tel):
        self.commodity_id = commodity_id
        self.status = status
        self.com = com
        self.time = time
        self.ini = ini
        self.des = des
        self.cur = cur
        self.person = person
        self.tel = tel


'''
农产品温湿度信息 (时间充足再来完善)
'''


class Monitor(db.Model):
    __tablename__ = 'monitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temp = db.Column(db.FLOAT, nullable=False)  # 温度
    hum = db.Column(db.FLOAT, nullable=False)  # 湿度
    date = db.Column(db.String(100), nullable=False)  # 时间

    def __init__(self, temp, hum, date):
        self.temp = temp
        self.hum = hum
        self.date = date


'''
区块链信息
'''


class Blockchain(db.Model):
    __tablename__ = 'blockchain'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    index = db.Column(db.Integer, nullable=False)  # 区块编号
    commodity_id = db.Column(db.String(255), nullable=False)  # 产品id，同时也作为区块链编号
    data = db.Column(db.Text, nullable=True)
    pre_hash = db.Column(db.String(255), nullable=True)
    cur_hash = db.Column(db.String(255), nullable=True)
    nonce = db.Column(db.String(255), nullable=True)  # 随机数
    timestamp = db.Column(db.String(100), nullable=True)  # 时间戳

    def __init__(self, index, commodity_id, data, pre_hash, cur_hash, nonce, timestamp):
        self.index = index
        self.commodity_id = commodity_id
        self.data = data
        self.pre_hash = pre_hash
        self.cur_hash = cur_hash
        self.nonce = nonce
        self.timestamp = timestamp



