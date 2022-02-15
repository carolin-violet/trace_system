"""
管理员管理用户信息
"""

from src.models import User
from flask import Blueprint, request, jsonify
from src.models import db

api = Blueprint('userInfo', __name__)


# 添加一个用户
@api.route('/users', methods=['POST'])
def add_user():
    phone = request.form['phone']
    role_id = request.form['role_id']
    password = request.form['password']
    name = request.form['name']
    gender = request.form['gender']
    identity_label = request.form['identity_label']
    address = request.form['address']
    email = request.form['email']

    if User.query.filter(User.phone == phone).first():
        return '用户已存在'
    else:
        user = User(role_id=role_id, phone=phone, password=password, name=name, gender=gender,
                    identity_label=identity_label,address=address, email=email)
        db.session.add(user)
        db.session.commit()
        return '添加成功'


# 删除单个用户
@api.route('/users/<phone>', methods=['DELETE'])
def del_user(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '删除成功'
    else:
        return '用户不存在'


# 修改单个用户的数据
@api.route('/users/<phone>', methods=['PATCH'])
def update_user(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        data = request.json
        for key in data.keys():
            if key == 'phone':
                user.phone = data['phone']
            if key == 'password':
                user.password = data['password']
            if key == 'name':
                user.name = data['name']
            if key == 'gender':
                user.gender = data['gender']
            if key == 'identity_label':
                user.identity_label = data['identity_label']
            if key == 'address':
                user.address = data['address']
            if key == 'email':
                user.email = data['email']
        db.session.commit()
        return '修改成功'
    else:
        return '用户不存在'


# 查询所有用户
@api.route('/users', methods=['GET'])
def query_user():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'phone': user.phone,
            'password': user.password,
            'name': user.name,
            'gender': user.gender,
            'identity_label': user.identity_label,
            'address': user.address,
            'email': user.email,
            })
    return jsonify(data)


# 查询单个用户
@api.route('/users/<phone>', methods=['GET'])
def all_users(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        return jsonify({
            'id': user.id,
            'phone': user.phone,
            'password': user.password,
            'name': user.name,
            'gender': user.gender,
            'identity_label': user.identity_label,
            'address': user.address,
            'email': user.email,
        })
    else:
        return '用户不存在'





