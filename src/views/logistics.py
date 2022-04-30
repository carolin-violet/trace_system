"""
物流信息模块
"""
from flask import Blueprint, request, jsonify
import time
from src.models import Logistics, db, User
from src.security import token_auth

logistics_page = Blueprint('logistics_page', __name__)


'''
添加物流信息 (同一产品在不同状态时都统一添加物流，前端获取信息修改后一并发过来)
'''


@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    transporter_id = request.json['transporter_id']

    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    role = User.query.filter(User.user_id == token_data['user_id']).first().role

    if (role=='admin' or role=='transporter') and token_data['user_id'] == transporter_id:
        pass
    else:
        return '权限不够'

    logistics_id = request.json['logistics_id']
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    status = request.json['status']
    cur = request.json['cur']

    logistics = Logistics(logistics_id, transporter_id, cur_time, status, cur)
    db.session.add(logistics)
    db.session.commit()

    return {
        "code": 0,
        "msg": '添加成功',
    }


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
