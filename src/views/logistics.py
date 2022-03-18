"""
物流信息模块
"""
from flask import Blueprint, request, jsonify
import time
from src.models import Logistics, db, TransportCmp
from src.security import token_auth

logistics_page = Blueprint('logistics_page', __name__)


'''
添加物流信息 (同一产品在不同状态时都统一添加物流，前端获取信息修改后一并发过来)
'''


@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    logistics_id = request.json['logistics_id']
    transporter_id = request.json['transporter_id']
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    status = request.json['status']
    cur = request.json['cur']

    logistics = Logistics(logistics_id, transporter_id, cur_time, status, cur)
    db.session.add(logistics)
    db.session.commit()

    return '添加成功'


'''
删除物流信息
'''


@logistics_page.route('/logistics/<logistics_id>', methods=['DELETE'])
def del_logistics(logistics_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = TransportCmp.query.filter(TransportCmp.staff_id == token_data['user_id']).first().role
    if role == 'manager':
        logistics = Logistics.query.filter(Logistics.logistics_id == logistics_id).first()
        if logistics:
            db.session.delete(logistics)
            db.session.commit()
            return '删除成功'
        else:
            return '物流不存在'
    else:
        return '无权限'


'''
查询指定产品的物流信息
'''


@logistics_page.route('/logistics/<logistics_id>', methods=['GET'])
def query_logistics(logistics_id):
    logistics_s = Logistics.query.filter(Logistics.logistics_id == logistics_id).all()
    if logistics_s:
        data = []
        for logistics in logistics_s:
            data.append({
                'transporter_id': logistics.transporter_id,
                'time': logistics.time,
                'status': logistics.status,
                'cur': logistics.cur,
            })
        return jsonify(data)
    else:
        return '物流不存在'
