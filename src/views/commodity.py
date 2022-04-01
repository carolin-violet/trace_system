"""
商品信息模块
"""
from flask import Blueprint, request, jsonify
from uuid import uuid1
import os
from src.models import Commodity, db, User
from src.utils import QR_code
from src.security import token_auth


commodity_page = Blueprint('commodity_page', __name__)


'''
添加商品信息
'''


@commodity_page.route('/commodity', methods=['POST'])
def add_commodity():
    producer_id = request.json['producer_id']
    area_id = int(request.json['area_id'])
    batch = int(request.json['batch'])
    name = request.json['name']
    weight = float(request.json['weight'])
    saler_id = request.json['saler_id']
    logistics_id = str(uuid1())
    ini = request.json['ini']
    des = request.json['des']

    qrcode_url = "http://127.0.0.1:5000" + "/commodity/detail/" + str(logistics_id) + '/' + str(saler_id)
    qr_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/qr_codes/'+logistics_id+'.png'
    QR_code.make_qrcode(qrcode_url, qr_path)

    commodity = Commodity(producer_id, area_id, batch, name, weight, saler_id, logistics_id, ini, des, qrcode_url)
    db.session.add(commodity)
    db.session.commit()

    return '添加成功'


'''
删除商品信息
'''


@commodity_page.route('/commodity/<logistics_id>', methods=['DELETE'])
def del_commodity(logistics_id):
    commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
    if commodity:
        db.session.delete(commodity)
        db.session.commit()
        return '删除成功'
    else:
        return '商品不存在'


'''
查询所有商品信息
'''


@commodity_page.route('/commodities', methods=['GET'])
def query_commodity():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data.role == 'admin':
        commodities = Commodity.query.all()
        data = []
        for commodity in commodities:
            data.append({
                'producer_id': commodity.producer_id,
                'area_id': commodity.area_id,
                'batch': commodity.batch,
                'name': commodity.name,
                'weight': commodity.weight,
                'saler_id': commodity.saler_id,
                'logistics_id': commodity.logistics_id,
                'ini': commodity.ini,
                'des': commodity.des,
                'qrcode_url': commodity.qrcode_url
            })
        return jsonify(data)
    else:
        return '无权限'




