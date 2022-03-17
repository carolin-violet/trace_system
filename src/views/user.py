"""
用户信息
"""
from flask import Blueprint, request, jsonify
from src.security import token_auth
from uuid import uuid1
from src.models import User, db
from src.security.RSA import create_keys


user_page = Blueprint('user_page', __name__)

'''
登录
'''


@user_page.route('/login', methods=['POST'])
def login():
    account = request.json['account']
    password = request.json['password']
    user = User.query.filter((User.phone == account) or (User.name == account)).first()
    token = token_auth.create_token(user.user_id)
    if user:
        if user.password == password:
            return {
                "msg": '登录成功',
                "token": token
            }
        else:
            return {
                "msg": '密码错误'
            }
    else:
        return {
                "msg": '用户不存在'
            }


'''
添加一个用户
'''


@user_page.route('/users', methods=['POST'])
def add_user():
    role_id = request.json['role_id']
    name = request.json['name']
    phone = request.json['phone']
    password = request.json['password']
    gender = request.json['gender']

    if User.query.filter(User.phone == phone).first():
        return '用户已存在'
    else:
        user_id = str(uuid1()).replace('-', '')
        public_key, private_key = create_keys()
        user = User(user_id, role_id, name, phone, password, gender, public_key, private_key)
        db.session.add(user)
        db.session.commit()
        return '注册成功'


'''
删除单个用户
'''


@user_page.route('/users/<phone>', methods=['DELETE'])
def del_user(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '删除成功'
    else:
        return '用户不存在'


'''
修改单个用户的密码
'''


@user_page.route('/users/password/<user_id>', methods=['PATCH'])
def update_user_password(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        password = request.json['password']
        user.password = password
        db.session.commit()
        return '修改成功'
    else:
        return '用户不存在'


'''
修改单个用户的手机号
'''


@user_page.route('/users/phone/<user_id>', methods=['PATCH'])
def update_user_phone(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        phone = request.json['phone']
        user.phone = phone
        db.session.commit()
        return '修改成功'
    else:
        return '用户不存在'


'''
查询所有用户
'''


@user_page.route('/users', methods=['GET'])
def query_user():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'user_id': user.user_id,
            'role_id': user.role_id,
            'name': user.name,
            'phone': user.phone,
            'password': user.password,
            'gender': user.gender,
            })
    return jsonify(data)


'''
查询单个用户
'''


@user_page.route('/users/<user_id>', methods=['GET'])
def all_users(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        return jsonify({
            'user_id': user.user_id,
            'role_id': user.role_id,
            'name': user.name,
            'phone': user.phone,
            'password': user.password,
            'gender': user.gender,
        })
    else:
        return '用户不存在'

