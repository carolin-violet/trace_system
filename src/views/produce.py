"""
生产信息
"""
import base64
from flask import Blueprint, request, jsonify, send_file
import time
import os
from src.security import token_auth
from src.models import Produce, db, User

produce_page = Blueprint('produce_page', __name__)

'''
添加生产信息
'''


@produce_page.route('/produce', methods=['POST'])
def add_produce_info():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        user_id = request.json['user_id']
        area_id = request.json['area_id']
        batch = request.json['batch']
        op_type = request.json['op_type']
        op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img = request.json['img']
        description = request.json['description']

        produce_info = Produce(user_id, area_id, batch, op_type, op_time, description, img)
        db.session.add(produce_info)
        db.session.commit()
        return '添加成功'
    else:
        return '无权限'


'''
查询指定生产商的生产信息
'''


@produce_page.route('/produce/<producer_id>', methods=['GET'])
def query_produce_info(producer_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        information = Produce.query.filter(Produce.user_id == producer_id).all()
        if not information:
            return "无生产信息"
        data = []
        for info in information:
            data.append({
                "area_id": info.area_id,
                "batch": info.batch,
                "op_type": info.op_type,
                "op_time": info.op_time,
                "description": info.description,
                "img": info.img,
            })
        return jsonify(data)
    else:
        return '无权限'


