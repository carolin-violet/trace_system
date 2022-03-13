"""
数据库模型
"""
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


'''
用户基本信息表
'''


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)  # 用户id
    role_id = db.Column(db.Integer, nullable=False)  # 用户角色,0为管理员,1为生产商,2为运输商,3为消费者
    name = db.Column(db.String(10), nullable=False)  # 姓名
    phone = db.Column(db.String(11), unique=True)  # 手机号码,用作登录账号
    password = db.Column(db.String(20), nullable=False)  # 登录密码
    gender = db.Column(db.String(6), nullable=False)  # 性别:male/female
    public_key = db.Column(db.VARBINARY(1000), nullable=False)  # 用户公钥
    private_key = db.Column(db.VARBINARY(1000), nullable=False)  # 用户私钥

    def __init__(self, user_id, role_id, name, phone, password, gender, public_key, private_key):
        self.user_id = user_id
        self.role_id = role_id
        self.name = name
        self.phone = phone
        self.password = password
        self.gender = gender
        self.public_key = public_key
        self.private_key = private_key

    def __repr__(self):
        return json.dumps({
            "user_id": self.user_id,
            "role_id": self.role_id,
            "name": self.name,
            "phone": self.phone,
            "password": self.password,
            "gender": self.gender,
            "public_key": str(self.public_key),
            "private_key": str(self.private_key)
        })


'''
生产信息表
'''


class Produce(db.Model):
    __tablename__ = 'produce'
    id = db.Column(db.Integer, autoincrement=True)
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域
    op_type = db.Column(db.String(2), nullable=False)  # 播种,浇水,施肥,除虫,除草,收割
    op_time = db.Column(db.DateTime, nullable=False)  # 操作时间
    description = db.Column(db.Text, default='')  # 详情描述
    img_path = db.Column(db.Text, default='')  # 照片存放地址

    def __init__(self, user_id, area_id, op_type, op_time, description, img_path):
        self.user_id = user_id
        self.area_id = area_id
        self.op_type = op_type
        self.op_time = op_time
        self.description = description
        self.img_path = img_path


'''
生产过程温湿度信息
'''


class ProduceMonitor(db.Model):
    __tablename__ = 'produce_monitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域
    temp = db.Column(db.FLOAT, nullable=False)  # 温度
    hum = db.Column(db.FLOAT, nullable=False)  # 湿度
    date = db.Column(db.String(100), nullable=False)  # 时间

    def __init__(self, user_id, area_id, temp, hum, date):
        self.user_id = user_id
        self.area_id = area_id
        self.temp = temp
        self.hum = hum
        self.date = date


'''
存储信息表
'''


class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, autoincrement=True)
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域
    repository_index = db.Column(db.Integer, nullable=False)  # 仓库区域编号
    in_time = db.Column(db.DateTime, nullable=False)  # 入库时间
    out_time = db.Column(db.DateTime, nullable=False)  # 出库时间
    description = db.Column(db.Text, default='')  # 详情描述
    img_path = db.Column(db.Text, default='')  # 照片存放地址

    def __init__(self, user_id, area_id, repository_index, in_time, out_time, description, img_path):
        self.user_id = user_id
        self.area_id = area_id
        self.repository_index = repository_index
        self.in_time = in_time
        self.out_time = out_time
        self.description = description
        self.img_path = img_path


'''
存储过程温湿度信息
'''


class StoreMonitor(db.Model):
    __tablename__ = 'store_monitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域
    repository_index = db.Column(db.Integer, nullable=False)  # 仓库区域编号
    temp = db.Column(db.FLOAT, nullable=False)  # 温度
    hum = db.Column(db.FLOAT, nullable=False)  # 湿度
    date = db.Column(db.String(100), nullable=False)  # 时间

    def __init__(self, user_id, area_id, repository_index, temp, hum, date):
        self.user_id = user_id
        self.area_id = area_id
        self.repository_index = repository_index
        self.temp = temp
        self.hum = hum
        self.date = date


'''
商品信息表
'''


class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, autoincrement=True)
    commodity_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    user_id = db.Column(db.String(255), nullable=False)  # 所属生产厂家用户id
    area = db.Column(db.Integer, nullable=False)  # 农田区域
    name = db.Column(db.String(10), nullable=False)  # 商品名称
    weight = db.Column(db.Float, nullable=True)  # 商品重量(斤)
    ini = db.Column(db.String(100), nullable=False)  # 初始地
    des = db.Column(db.String(100), nullable=False)  # 目的地
    qrcode_url = db.Column(db.Text, nullable=False)  # 二维码存放的网址
    cur_hash = db.Column(db.String(255), nullable=False)  # 此产品对应区块链的当前hash值，作为区块链的索引

    def __init__(self, commodity_id, user_id, area, name, weight, ini, des, qrcode_url, cur_hash=''):
        self.commodity_id = commodity_id
        self.user_id = user_id
        self.area = area
        self.name = name
        self.weight = weight
        self.ini = ini
        self.des = des
        self.qrcode_url = qrcode_url
        self.cur_hash = cur_hash

    def __repr__(self):
        return '<Commodity %r>' % self.commodity_id


'''
物流信息
'''


class Logistics(db.Model):
    __tablename__ = 'logistics'
    id = db.Column(db.Integer, autoincrement=True)
    commodity_id = db.Column(db.String(255), primary_key=True, nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    status = db.Column(db.String(10), nullable=False)  # 商品状态  (已发货, 运输中, 已到货, 已签收)
    com = db.Column(db.String(50), nullable=False)  # 操作的公司名
    time = db.Column(db.String(100), nullable=False)  # 操作时间，需要获取当前系统时间
    cur = db.Column(db.String(100), nullable=False)  # 当前所在地
    person = db.Column(db.String(20), nullable=False)  # 操作人
    tel = db.Column(db.String(11), nullable=False)  # 操作人联系方式

    def __init__(self, commodity_id, status, com, time, cur, person, tel):
        self.commodity_id = commodity_id
        self.status = status
        self.com = com
        self.time = time
        self.cur = cur
        self.person = person
        self.tel = tel


'''
区块链信息
'''


class Blockchain(db.Model):
    __tablename__ = 'blockchain'
    id = db.Column(db.BIGINT, autoincrement=True,)
    cur_hash = db.Column(db.String(255), primary_key=True, nullable=True)  # 当前区块data的hash值，作为主键
    pre_hash = db.Column(db.String(255), nullable=True)  # 前一个区块的hash值
    timestamp = db.Column(db.String(100), nullable=True)  # 时间戳
    nonce = db.Column(db.BIGINT, nullable=False)  # 随机数
    data = db.Column(db.Text, nullable=True)  # 数据部分

    def __init__(self, pre_hash, cur_hash, timestamp, nonce, data):
        self.pre_hash = pre_hash
        self.cur_hash = cur_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.data = data



