"""
用户信息
"""
from flask import Blueprint
from src.models import User


statistics_page = Blueprint('statistics_page', __name__)

'''
登录
'''


@statistics_page.route('/statistics/personCount', methods=['GET'])
def login():
    admin_count = User.query.filter(User.role == 'admin').count()
    producer_count = User.query.filter(User.role == 'producer').count()
    transporter_count = User.query.filter(User.role == 'transporter').count()
    saler_count = User.query.filter(User.role == 'saler').count()

    data = [
        {"name": '管理者', "value": admin_count},
        {"name": '生产者', "value": producer_count},
        {"name": '运输人员', "value": transporter_count},
        {"name": '销售商', "value": saler_count}
    ]
    return {
        "code": 0,
        "msg": "获取成功",
        "data": data
    }

