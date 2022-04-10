"""
用户信息
"""
from flask import Blueprint, request, jsonify
from src.security import token_auth
from src.models import User, db


statistics_page = Blueprint('statistics_page', __name__)

'''
登录
'''


@statistics_page.route('/statistics/personCount', methods=['GET'])
def login():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    admin_count = User.query.filter(User.role == 'admin').count()
    producer_count = User.query.filter(User.role == 'producer').count()
    transporter_count = User.query.filter(User.role == 'transporter').count()
    saler_count = User.query.filter(User.role == 'saler').count()

    counts = {
        "xData": ["管理者", "生产商", "运输人员", "销售商"],
        "yData": [admin_count, producer_count, transporter_count, saler_count]
    }
    return counts

