"""
物流信息模块
"""
from src.models import Logistics, Blockchain, db
from src.utils import blockchain
from flask import Blueprint, request, jsonify
import time

logistics_page = Blueprint('logistics_page', __name__)


# 添加物流信息 (同一产品在不同状态时都统一添加物流，前端获取信息修改后一并发过来)
@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    product_id = request.form['product_id']
    status = request.form['status']
    com = request.form['com']
    ini = request.form['ini']
    des = request.form['des']
    cur = request.form['cur']
    person = request.form['person']
    tel = request.form['tel']
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if Logistics.query.filter(Logistics.product_id == product_id).first():
        return '物流已存在'
    else:
        block = blockchain.Chain(product_id)
        blocks = Blockchain.query.filter(Blockchain.commodity_id == product_id).all()
        if not blocks:
            block.create_genesis_block(db)
        logistics = Logistics(product_id, status, com, cur_time, ini, des, cur, person, tel)
        db.session.add(logistics)
        db.session.commit()
        return '添加成功'


# 删除物流信息
@logistics_page.route('/logistics/<id>', methods=['DELETE'])
def del_logistics(id):
    logistics = Logistics.query.filter(Logistics.id == id).first()
    if logistics:
        db.session.delete(logistics)
        db.session.commit()
        return '删除成功'
    else:
        return '物流不存在'


# 查询指定产品的物流信息
@logistics_page.route('/logistics/<product_id>', methods=['GET'])
def query_logistics(product_id):
    logistics_s = Logistics.query.filter(Logistics.product_id == product_id).all()
    if logistics_s:
        data = []
        for logistics in logistics_s:
            data.append({
                "id": logistics.id,
                'product_id': logistics.product_id,
                'status': logistics.status,
                'com': logistics.com,
                'time': logistics.time,
                'ini': logistics.ini,
                'des': logistics.des,
                'cur': logistics.cur,
                'person': logistics.person,
                'tel': logistics.tel,
            })
        return jsonify(data)
    else:
        return '物流不存在'
