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


@user_page.route('/user/login', methods=['POST'])
def login():
    tel = request.json['username']  # 姓名或者手机号
    password = request.json['password']
    user = User.query.filter(User.tel == tel).first()
    if user:
        if user.password == password:
            token = token_auth.create_token(user.user_id)
            user.token = token
            db.session.commit()
            return {
                "code": 0,
                "message": "认证成功",
                "data": {"token": token}
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
获取用户信息
'''


@user_page.route('/user/user_info', methods=['GET'])
def get_user_info():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    user = User.query.filter(User.user_id == token_data['user_id']).first()
    if user:
        return {
            "code": 0,
            "msg": "认证成功",
            "data": {
                "roles": user.role,
                "name": user.name,
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
            }
        }


'''
注销
'''


@user_page.route('/user/logout', methods=['GET'])
def logout():
    return ''


'''
注册(添加)用户
'''


@user_page.route('/users', methods=['POST'])
def add_user():
    role = request.json['role']
    name = request.json['name']
    tel = request.json['tel']
    password = request.json['password']
    gender = request.json['gender']

    if User.query.filter(User.tel == tel).first():
        return '该手机号已被注册'
    else:
        user_id = str(uuid1()).replace('-', '')
        public_key, private_key = create_keys()
        user = User(user_id, role, name, tel, password, gender, public_key, private_key)
        db.session.add(user)
        db.session.commit()
        return {
            "code": 0,
            "msg": '添加成功'
        }


'''
删除单个用户
'''


@user_page.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {
            "code": 0,
            "msg": '删除成功'
        }
    else:
        return '用户不存在'


'''
修改单个用户信息
'''


@user_page.route('/users/info/<user_id>', methods=['PATCH'])
def update_user_info(user_id):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        user.name = request.json['name']
        user.password = request.json['password']
        user.tel = request.json['tel']
        user.gender = request.json['gender']
        db.session.commit()
        return {
            "code": 0,
            "msg": '修改成功'
        }
    else:
        return '用户不存在'


'''
查询不同类型的人
'''


@user_page.route('/users/<user_type>', methods=['GET'])
def query_producer(user_type):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if user_type == 'all':
        users = User.query.all()
    else:
        users = User.query.filter(User.role == user_type).all()
    data = []
    for user in users:
        data.append({
            'user_id': user.user_id,
            'role': user.role,
            'name': user.name,
            'tel': user.tel,
            'password': user.password,
            'gender': user.gender,
            })
    return jsonify(data)




