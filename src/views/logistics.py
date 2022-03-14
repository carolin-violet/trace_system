"""
物流信息模块
"""
from flask import Blueprint, request, jsonify
import time
from src.models import Logistics, db

logistics_page = Blueprint('logistics_page', __name__)


'''
添加物流信息 (同一产品在不同状态时都统一添加物流，前端获取信息修改后一并发过来)
'''


@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    logistics_id = request.form['logistics_id']
    status = request.form['status']
    com = request.form['com']
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cur = request.form['cur']
    person = request.form['person']
    tel = request.form['tel']

    logistics = Logistics(logistics_id, status, com, cur_time, cur, person, tel)
    db.session.add(logistics)
    db.session.commit()

    return '添加成功'


'''
删除物流信息
'''


@logistics_page.route('/logistics/<logistics_id>', methods=['DELETE'])
def del_logistics(logistics_id):
    logistics = Logistics.query.filter(Logistics.logistics_id == logistics_id).first()
    if logistics:
        db.session.delete(logistics)
        db.session.commit()
        return '删除成功'
    else:
        return '物流不存在'


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
                'status': logistics.status,
                'com': logistics.com,
                'time': logistics.time,
                'cur': logistics.cur,
                'person': logistics.person,
                'tel': logistics.tel,
            })
        return jsonify(data)
    else:
        return '物流不存在'
