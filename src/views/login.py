"""
登录模块
"""
from src.models import User
from flask import Blueprint, request

api = Blueprint('login', __name__)


@api.route('/login', methods=['POST'])
def login():
    account = request.json['account']
    password = request.json['password']
    user = User.query.filter(User.phone == account).first()
    if user:
        if user.password == password:
            return {
                "msg": '登录成功',
                "info": {
                    "phone": user.phone,
                    "nickName": user.nickName
                }
            }
        else:
            return {
                "msg": '密码错误'
            }
    else:
        return {
                "msg": '用户不存在'
            }



