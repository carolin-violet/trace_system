"""
登录模块
"""
from src.models import User
from flask import Blueprint, request

login_page = Blueprint('login_page', __name__)


@login_page.route('/login', methods=['POST'])
def login():
    account = request.json['account']
    password = request.json['password']
    user = User.query.filter((User.phone == account) or (User.name == account)).first()
    if user:
        if user.password == password:
            return {
                "msg": '登录成功',
                "info": {
                    "phone": user.phone,
                    "name": user.name
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



