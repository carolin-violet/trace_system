"""
管理员管理用户信息
"""

from src.models import User
from flask import Blueprint, request, jsonify
from src.extension import db

user_page = Blueprint('user_page', __name__)


# 添加一个用户
@user_page.route('/users', methods=['POST'])
def add_user():
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    gender = request.form['gender']

    if User.query.filter(User.phone == phone).first():
        return '用户已存在'
    else:
        user = User(name, phone, password, gender)
        db.session.add(user)
        db.session.commit()
        return '添加成功'


# 删除单个用户
@user_page.route('/users/<phone>', methods=['DELETE'])
def del_user(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '删除成功'
    else:
        return '用户不存在'


# 修改单个用户的数据
@user_page.route('/users/<phone>', methods=['PATCH'])
def update_user(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        data = request.json
        for key in data.keys():
            if key == 'name':
                user.name = data['name']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'password':
                user.password = data['password']
            if key == 'gender':
                user.gender = data['gender']
        db.session.commit()
        return '修改成功'
    else:
        return '用户不存在'


# 查询所有用户
@user_page.route('/users', methods=['GET'])
def query_user():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'password': user.password,
            'gender': user.gender,
            })
    return jsonify(data)


# 查询单个用户
@user_page.route('/users/<phone>', methods=['GET'])
def all_users(phone):
    user = User.query.filter(User.phone == phone).first()
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'password': user.password,
            'gender': user.gender,
        })
    else:
        return '用户不存在'





