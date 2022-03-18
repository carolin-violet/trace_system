"""
商品信息模块
"""
from flask import Blueprint, request, jsonify, send_file
from uuid import uuid1
import os
from src.models import Commodity, db, User
from src.utils import img
from src.security import token_auth


commodity_page = Blueprint('commodity_page', __name__)


'''
添加商品信息
'''


@commodity_page.route('/commodity', methods=['POST'])
def add_commodity():
    user_id = request.json['user_id']
    area_id = int(request.json['area_id'])
    batch = int(request.json['batch'])
    name = request.json['name']
    weight = float(request.json['weight'])
    saler_id = float(request.json['saler_id'])
    logistics_id = str(uuid1())
    ini = request.json['ini']
    des = request.json['des']

    qrcode_url = "http://127.0.0.1:5000" + "/commodity/" + str(logistics_id) + '/' + str(saler_id)
    qr_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/qr_codes/'+logistics_id+'.png'
    img.make_qrcode(qrcode_url, qr_path)

    commodity = Commodity(user_id, area_id, batch, name, weight, saler_id, logistics_id, ini, des, qrcode_url)
    db.session.add(commodity)
    db.session.commit()

    return '添加成功'


'''
删除商品信息
'''


@commodity_page.route('/commodity/<logistics_id>', methods=['DELETE'])
def del_commodity(logistics_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'producer' or 'admin':
        commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
        if commodity:
            db.session.delete(commodity)
            db.session.commit()
            return '删除成功'
        else:
            return '商品不存在'
    else:
        return '无权限'


'''
查询所有商品信息
'''


@commodity_page.route('/commodity', methods=['GET'])
def query_commodity():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        commodities = Commodity.query.all()
        data = []
        for commodity in commodities:
            data.append({
                'user_id': commodity.user_id,
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


'''
查询指定id商品信息
'''


@commodity_page.route('/commodity/<logistics_id>', methods=['GET'])
def get_commodity(logistics_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
        if commodity:
            return jsonify({
                'user_id': commodity.user_id,
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
        else:
            return '商品不存在'
    else:
        return '无权限'




