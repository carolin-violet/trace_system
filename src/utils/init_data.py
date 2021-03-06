from uuid import uuid1
from src.models import User
from src.security.RSA import create_keys
from src.utils.chain import Chain
from src.utils.create_tel import create_tel


def initialize(db):
    print('-------------------正在创建数据库表------------------')
    # 创建表
    db.create_all()

    init_user(db)

    '''
    创建初始区块
    '''
    blockchain = Chain('', db)
    blockchain.create_genesis_block()

    print('-------------------创建数据库表完成------------------')
    return 'success'


'''
初始化用户表
'''


def init_user(db):
    # 创建管理员账户
    public_key, private_key = create_keys()
    admin = User('0', 'admin', 'admin', 'admin', '123456', '男', public_key, private_key)

    # 创建生产商账户
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    producer1 = User(user_id, 'producer', '萧永元', tel, '123456', '男', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    producer2 = User(user_id, 'producer', '空刚毅', tel, '123456', '女', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    producer3 = User(user_id, 'producer', '桓乐意', tel, '123456', '男', public_key, private_key)

    # 创建运输商账户
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter1 = User(user_id, 'transporter', '厍博学', tel, '123456', '男', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter2 = User(user_id, 'transporter', '顾高义', tel, '123456', '女', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter3 = User(user_id, 'transporter', '傅承弼', tel, '123456', '男', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter4 = User(user_id, 'transporter', '苏睿明', tel, '123456', '男', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter5 = User(user_id, 'transporter', '幸宏富', tel, '123456', '女', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    transporter6 = User(user_id, 'transporter', '芮华灿', tel, '123456', '男', public_key, private_key)

    # 创建销售商账户
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    saler1 = User(user_id, 'saler', '符德华', tel, '123456', '男', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    saler2 = User(user_id, 'saler', '堵星文', tel, '123456', '女', public_key, private_key)
    public_key, private_key = create_keys()
    user_id = str(uuid1()).replace('-', '')
    tel = create_tel()
    saler3 = User(user_id, 'saler', '宰俊良', tel, '123456', '男', public_key, private_key)

    db.session.add_all([admin, producer1, producer2, producer3, transporter1, transporter2, transporter3, transporter4,
                    transporter5, transporter6, saler1, saler2, saler3])
    db.session.commit()

