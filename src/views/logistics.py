"""
物流信息模块
"""
from src.models import Logistics, Blockchain, db
from src.utils import chain, img
from flask import Blueprint, request, jsonify
import time
import json

logistics_page = Blueprint('logistics_page', __name__)


'''
添加物流信息 (同一产品在不同状态时都统一添加物流，前端获取信息修改后一并发过来)
'''


@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    commodity_id = request.form['commodity_id']
    status = request.form['status']
    com = request.form['com']
    ini = request.form['ini']
    des = request.form['des']
    cur = request.form['cur']
    person = request.form['person']
    tel = request.form['tel']
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    '''
    添加物流
    '''
    logistics = Logistics(commodity_id, status, com, cur_time, ini, des, cur, person, tel)
    db.session.add(logistics)
    db.session.commit()

    '''
    添加区块
    '''
    blocks = Blockchain.query.filter(Blockchain.commodity_id == commodity_id).all()
    block = chain.Chain(commodity_id, blocks)

    if not blocks:
        block.create_genesis_block(db)
    block.add_block(db, commodity_id, status, com, cur_time, ini, des, cur, person, tel)

    '''
    添加二维码信息
    '''
    data = {
        "商品id": commodity_id,
        "始发地": ini,
        "目的地": des,
        "运输信息": []
    }
    for item in blocks[1:-1]:
        data['运输信息'].append({
            "时间": item.time,
            "状态": item.status,
            "操作公司": item.com,
            "当前所在地": item.cur,
            "操作人": item.person,
            "操作人电话": item.tel
        })
    img.make_qrcode('../../static/qr_codes/', commodity_id, json.dumps(data, sort_keys=True))
    return '添加成功'


'''
删除物流信息
'''


@logistics_page.route('/logistics/<id>', methods=['DELETE'])
def del_logistics(id):
    logistics = Logistics.query.filter(Logistics.id == id).first()
    if logistics:
        db.session.delete(logistics)
        db.session.commit()
        return '删除成功'
    else:
        return '物流不存在'


'''
查询指定产品的物流信息
'''


@logistics_page.route('/logistics/<commodity_id>', methods=['GET'])
def query_logistics(commodity_id):
    logistics_s = Logistics.query.filter(Logistics.commodity_id == commodity_id).all()
    if logistics_s:
        data = []
        for logistics in logistics_s:
            data.append({
                "id": logistics.id,
                'commodity_id': logistics.commodity_id,
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
