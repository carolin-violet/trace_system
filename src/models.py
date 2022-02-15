from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''数据库模型'''


# 用户基本信息表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), unique=True)  # 手机号码,用作登录账号,用作主键
    password = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(6), nullable=False)  # 性别:male/female

    def __init__(self, name, phone, password, gender):
        self.name = name
        self.phone = phone
        self.password = password
        self.gender = gender

    def __repr__(self):
        return '<User %r>' % self.userName


# 商品信息表
class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)  # 商品名称
    price = db.Column(db.Integer, nullable=False)  # 商品单价
    weight = db.Column(db.String(10), nullable=True)  # 商品重量
    status = db.Column(db.String(10), nullable=False)  # 商品状态
    product_id = db.Column(db.String(255), nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    block_info = db.Column(db.Text, default='')  # 二维码信息

    def __init__(self, name, price, weight, status, product_id, block_info=''):
        self.name = name
        self.price = price
        self.weight = weight
        self.status = status
        self.product_id = product_id
        self.block_info = block_info

    def __repr__(self):
        return '<Commodity %r>' % self.name


# 运输信息
class Transport(db.Model):
    __tablename__ = 'transport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(255), nullable=False)  # 编号（ 物流：运单号  仓库：仓库编号）
    com = db.Column(db.String(50), nullable=False)  # 操作的公司名
    time = db.Column(db.String(100), nullable=False)  # 操作时间，需要获取当前系统时间
    ini = db.Column(db.String(100), nullable=False)  # 初始地
    des = db.Column(db.String(100), nullable=False)  # 目的地
    person = db.Column(db.String(20), nullable=False)  # 操作人
    tel = db.Column(db.String(30), nullable=False)  # 操作人联系方式

    def __init__(self, product_id, com, time, ini, des, person, tel):
        self.product_id = product_id
        self.com = com
        self.time = time
        self.ini = ini
        self.des = des
        self.person = person
        self.tel = tel


# 农产品温湿度信息 (时间充足再来完善)
class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temp = db.Column(db.FLOAT, nullable=False)  # 温度
    hum = db.Column(db.FLOAT, nullable=False)  # 湿度
    date = db.Column(db.String(100), nullable=False)  # 时间

    def __init__(self, temp, hum, date):
        self.temp = temp
        self.hum = hum
        self.date = date


# 区块链信息
class Blockchain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(100), nullable=False)  # 索引
    commodity_id = db.Column(db.Integer, nullable=False)
    commodity_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=True)
    pre_hash = db.Column(db.String(255), nullable=True)
    cur_hash = db.Column(db.String(255), nullable=True)
    nonce = db.Column(db.String(255), nullable=True)  # 随机数

    def __init__(self, index, commodity_id, commodity_name, data, prehash, curhash, nonce):
        self.index = index
        self.commodity_id = commodity_id
        self.commodity_name = commodity_name
        self.data = data
        self.prehash = prehash
        self.curhash = curhash
        self.nonce = nonce