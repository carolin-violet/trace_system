from src.models import User


def initialize(db):

    # 创建表
    db.create_all()

    admin = User('admin', '17075256495', '123456', 'male')
    db.session.add(admin)
    db.session.commit()

