"""
生产信息
"""
from flask import Blueprint, request, jsonify
import time
from src.security import token_auth
from src.models import Produce, db, User
from src.utils.duplicate_remove import unique_data
import os

produce_page = Blueprint('produce_page', __name__)

'''
添加生产信息
'''


@produce_page.route('/produce', methods=['POST'])
def add_produce():
    user_id = request.json['user_id']

    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'admin' or token_data['user_id'] == user_id:
        pass
    else:
        return '权限不够'

    area_id = request.json['area_id']
    batch = request.json['batch']
    op_type = request.json['op_type']
    op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    img = request.json['img']
    description = request.json['description']

    img_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/produce_img/' + str(user_id) + '-' + str(area_id) + '-' + str(batch) + '-' + str(time.time()) + '.txt'
    with open(img_path, 'w') as fp:
        fp.write(img)

    produce_info = Produce(user_id, area_id, batch, op_type, op_time, description, img_path)
    db.session.add(produce_info)
    db.session.commit()
    return {
        "code": 0,
        "msg": '添加成功'
    }


'''
查询指定生产商的生产信息汇总
'''


@produce_page.route('/produce/<producer_id>', methods=['GET'])
def query_produce_detail(producer_id):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'admin' or token_data['user_id'] == producer_id:
        pass
    else:
        return '权限不够'

    information = Produce.query.filter(Produce.producer_id == producer_id).all()
    if not information:
        return "无生产信息"
    data = []
    for info in information:
        data.append({
            "user_id": producer_id,
            "area_id": info.area_id,
            "batch": info.batch
        })
    return jsonify(unique_data(data))


'''
查询指定生产商的生产信息详情
'''


@produce_page.route('/produce/<producer_id>/<area_id>/<batch>', methods=['GET'])
def query_produce_summary(producer_id, area_id, batch):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'admin' or token_data['user_id'] == producer_id:
        pass
    else:
        return '权限不够'

    information = Produce.query.filter(Produce.producer_id == producer_id, Produce.area_id == area_id, Produce.batch == batch).all()
    if not information:
        return "无生产信息"
    data = []
    for info in information:

        with open(info.img_path, 'r') as fp:
            data.append({
                "op_type": info.op_type,
                "op_time": info.op_time,
                "description": info.description,
                "img": fp.read(),
            })
    return jsonify(data)

