"""
用户信息
"""
from flask import Blueprint, request, jsonify
from src.security import token_auth
from uuid import uuid1
from src.models import User, db, TransportCmp
from src.security.RSA import create_keys


user_page = Blueprint('user_page', __name__)

'''
登录
'''


@user_page.route('/login', methods=['POST'])
def login():
    tel = request.json['tel']  # 姓名或者手机号
    password = request.json['password']
    user = User.query.filter(User.tel == tel).first()
    if user:
        if user.password == password:
            token = token_auth.create_token(user.user_id)
            user.token = token
            db.session.commit()
            return {
                "msg": '登录成功',
                "profile": {
                    "user_id": user.user_id,
                    "role": user.role,
                    "name": user.name,
                    "tel": user.tel,
                    "gender": user.gender,
                    "token": user.token,
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


'''
注册用户
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
        user = User(user_id, role, name, tel, password, gender, public_key, private_key, '')
        db.session.add(user)
        db.session.commit()
        return '成功'


'''
删除单个用户
'''


@user_page.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return '删除成功'
        else:
            return '用户不存在'
    else:
        return '无权限'


'''
修改单个用户信息
'''


@user_page.route('/users/info/<user_id>', methods=['PATCH'])
def update_user_info(user_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0' or user_id:
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            name = request.json['name']
            password = request.json['password']
            tel = request.json['tel']
            gender = request.json['gender']
            user.name = name
            user.password = password
            user.tel = tel
            user.gender = gender
            db.session.commit()
            return '修改成功'
        else:
            return '用户不存在'
    else:
        return '无权限'


'''
查询所有生产商
'''


@user_page.route('/users/producer', methods=['GET'])
def query_producer():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    if token_data['user_id'] == '0':
        users = User.query.filter(User.role == 'producer').all()
        data = []
        for user in users:
            data.append({
                'user_id': user.user_id,
                'name': user.name,
                'tel': user.tel,
                'password': user.password,
                'gender': user.gender,
                })
        return jsonify(data)
    else:
        return '无权限'


# '''
# 查询所有运输公司
# '''
#
#
# @user_page.route('/users/transporter', methods=['GET'])
# def query_transport_company():
#     token_data = token_auth.verify_token(request.headers['token'])
#     if token_data == 'token过期或错误':
#         return '请重新登录'
#
#     if token_data['user_id'] == '0':
#         company_s = TransportCmp.query.filter(TransportCmp.staff_role == 'manager').all()
#         data = []
#         for company in company_s:
#             data.append({
#                 "company_name": company.company_name,
#                 "manager_id": company.staff_id,
#                 "manager_name": company.staff_name,
#                 "manager_tel": company.staff_tel
#             })
#     else:
#         return '无权限'


'''
查询所有销售商
'''


@user_page.route('/users/saler', methods=['GET'])
def query_saler():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    if token_data['user_id'] == '0':
        users = User.query.filter(User.role == 'saler').all()
        data = []
        for user in users:
            data.append({
                'user_id': user.user_id,
                'name': user.name,
                'tel': user.tel,
                'password': user.password,
                'gender': user.gender,
                })
        return jsonify(data)
    else:
        return '无权限'


'''
查询单个用户
'''


@user_page.route('/user/<user_id>', methods=['GET'])
def all_users(user_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0' or user_id:
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            return jsonify({
                'user_id': user.user_id,
                'role': user.role,
                'name': user.name,
                'tel': user.tel,
                'password': user.password,
                'gender': user.gender,
            })
        else:
            return '用户不存在'
    else:
        return '无权限'

