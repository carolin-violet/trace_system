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
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '删除成功'
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


'''
查询所有生产商
'''


@user_page.route('/users/producer', methods=['GET'])
def query_producer():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
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


'''
查询所有运输人员信息
'''


@user_page.route('/users/transporter', methods=['GET'])
def query_transport_company():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    users = User.query.filter(User.role == 'transporter').all()
    data = []
    for user in users:
        company_info = TransportCmp.query.filter(TransportCmp.staff_id == user.user_id).first()
        if company_info:
            data.append({
                'user_id': user.user_id,
                'name': user.name,
                'tel': user.tel,
                'password': user.password,
                'gender': user.gender,
                'company_name': company_info.company_name,
                'staff_role': company_info.staff_role,
                })
        elif not company_info:
            data.append({
                'user_id': user.user_id,
                'name': user.name,
                'tel': user.tel,
                'password': user.password,
                'gender': user.gender,
                'company_name': '无',
                'staff_role': '无',
            })
    return jsonify(data)


'''
查询所有销售商
'''


@user_page.route('/users/saler', methods=['GET'])
def query_saler():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
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



