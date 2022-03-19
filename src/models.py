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
    user_id = db.Column(db.String(255), nullable=False)  # 用户id
    role = db.Column(db.String(15), nullable=False)  # 用户角色,admin为管理员,producer为生产商,transporter为运输商,saler为销售者
    name = db.Column(db.String(15), nullable=False)  # 姓名
    tel = db.Column(db.String(11), unique=True)  # 手机号码,用作登录账号
    password = db.Column(db.String(20), nullable=False)  # 登录密码
    gender = db.Column(db.String(6), nullable=False)  # 性别:male/female
    public_key = db.Column(db.VARBINARY(1000), nullable=False)  # 用户公钥
    private_key = db.Column(db.VARBINARY(1000), nullable=False)  # 用户私钥
    token = db.Column(db.String(255), nullable=False)  # 用户token

    def __init__(self, user_id, role, name, tel, password, gender, public_key, private_key, token):
        self.user_id = user_id
        self.role = role
        self.name = name
        self.tel = tel
        self.password = password
        self.gender = gender
        self.public_key = public_key
        self.private_key = private_key
        self.token = token


'''
生产信息表
'''


class Produce(db.Model):
    __tablename__ = 'produce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域id
    batch = db.Column(db.Integer, nullable=False)  # 生产批次
    op_type = db.Column(db.String(2), nullable=False)  # 播种,浇水,施肥,除虫,除草,收割,存储,出库
    op_time = db.Column(db.String(100), nullable=False)  # 操作时间
    description = db.Column(db.Text, default='')  # 详情描述
    img_path = db.Column(db.Text, default='')  # 照片存放地址

    def __init__(self, user_id, area_id, batch, op_type, op_time, description, img_path=''):
        self.user_id = user_id
        self.area_id = area_id
        self.batch = batch
        self.op_type = op_type
        self.op_time = op_time
        self.description = description
        self.img_path = img_path


'''
生产过程温湿度信息
'''


class TH(db.Model):
    __tablename__ = 'th'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)  # 生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域id
    batch = db.Column(db.Integer, nullable=False)  # 生产批次
    temp = db.Column(db.FLOAT, nullable=False)  # 温度
    hum = db.Column(db.FLOAT, nullable=False)  # 湿度
    date = db.Column(db.String(100), nullable=False)  # 时间

    def __init__(self, user_id, area_id, batch, temp, hum, date):
        self.user_id = user_id
        self.area_id = area_id
        self.batch = batch
        self.temp = temp
        self.hum = hum
        self.date = date


'''
商品信息表
'''


class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), nullable=False)  # 所属生产厂家用户id
    area_id = db.Column(db.Integer, nullable=False)  # 农田区域
    batch = db.Column(db.Integer, nullable=False)  # 生产批次
    name = db.Column(db.String(10), nullable=False)  # 商品名称
    weight = db.Column(db.Float, nullable=True)  # 商品重量(斤)
    saler_id = db.Column(db.String(255), nullable=False)  # 销售商id
    logistics_id = db.Column(db.String(255), nullable=False)  # 物流单号
    ini = db.Column(db.String(100), nullable=False)  # 初始地
    des = db.Column(db.String(100), nullable=False)  # 目的地
    qrcode_url = db.Column(db.Text, nullable=False)  # 二维码存放的网址

    def __init__(self, user_id, area_id, batch, name, weight, saler_id, logistics_id, ini, des, qrcode_url):
        self.user_id = user_id
        self.area_id = area_id
        self.batch = batch
        self.name = name
        self.weight = weight
        self.saler_id = saler_id
        self.logistics_id = logistics_id
        self.ini = ini
        self.des = des
        self.qrcode_url = qrcode_url

    def __repr__(self):
        return '<Commodity %r>' % self.logistics_id


'''
运输公司信息
'''


class TransportCmp(db.Model):
    __tablename__ = 'transport_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50), nullable=False)  # 公司名
    staff_id = db.Column(db.String(255), nullable=False)  # 员工id
    staff_role = db.Column(db.String(10), nullable=False)  # 员工职位 manager为管理者,common为普通员工
    staff_name = db.Column(db.String(20), nullable=False)  # 员工姓名
    staff_tel = db.Column(db.String(11), nullable=False)  # 员工联系方式

    def __init__(self, company_name, staff_id, staff_role, staff_name, staff_tel):
        self.company_name = company_name
        self.staff_id = staff_id
        self.staff_role = staff_role
        self.staff_name = staff_name
        self.staff_tel = staff_tel


'''
物流信息
'''


class Logistics(db.Model):
    __tablename__ = 'logistics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logistics_id = db.Column(db.String(255), nullable=False)  # 物流单号
    transporter_id = db.Column(db.String(255), nullable=False)  # 操作人id
    time = db.Column(db.String(100), nullable=False)  # 操作时间，需要获取当前系统时间
    status = db.Column(db.String(10), nullable=False)  # 商品状态  (已发货, 运输中, 已到货)
    cur = db.Column(db.String(100), nullable=False)  # 当前所在地

    def __init__(self, logistics_id, transporter_id, time, status, cur):
        self.logistics_id = logistics_id
        self.transporter_id = transporter_id
        self.time = time
        self.status = status
        self.cur = cur


'''
区块链信息
'''


class Blockchain(db.Model):
    __tablename__ = 'blockchain'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True,)
    logistics_id = db.Column(db.String(255), nullable=False)  # 物流单号
    cur_hash = db.Column(db.String(255), nullable=True)  # 当前区块的hash值
    pre_hash = db.Column(db.String(255), nullable=True)  # 前一个区块的hash值
    timestamp = db.Column(db.String(100), nullable=True)  # 时间戳
    nonce = db.Column(db.BIGINT, nullable=False)  # 随机数
    data_path = db.Column(db.String(255), nullable=True)  # 数据部分,存储加密数据所在文件路径

    def __init__(self, logistics_id, cur_hash, pre_hash, timestamp, nonce, data_path):
        self.logistics_id = logistics_id
        self.cur_hash = cur_hash
        self.pre_hash = pre_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.data_path = data_path



