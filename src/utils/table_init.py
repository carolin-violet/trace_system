from src.models import User
from src.security.RSA import create_keys


def initialize(db):

    # 创建表
    db.create_all()

    # 创建管理员账户
    public_key, private_key = create_keys()
    admin = User('0', '0', 'admin', '17075256495', '123456', 'male', public_key, private_key)
    db.session.add(admin)
    db.session.commit()



