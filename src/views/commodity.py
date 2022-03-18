"""
商品信息模块
"""
from flask import Blueprint, request, jsonify, send_file
from uuid import uuid1
import os
from src.models import Commodity, db
from src.utils import img
from src.security import token_auth


commodity_page = Blueprint('commodity_page', __name__)


'''
添加商品信息
'''


@commodity_page.route('/commodity', methods=['POST'])
def add_commodity():
    user_id = request.form['user_id']
    area_id = int(request.form['area_id'])
    batch = int(request.form['batch'])
    name = request.form['name']
    price = float(request.form['price'])
    weight = float(request.form['weight'])
    logistics_id = str(uuid1())
    ini = request.form['ini']
    des = request.form['des']

    qrcode_url = "http://127.0.0.1:5000" + "/purchase/" + str(logistics_id)
    qr_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/qr_codes/'+logistics_id+'.png'
    img.make_qrcode(qrcode_url, qr_path)

    commodity = Commodity(user_id, area_id, batch, name, price, weight, logistics_id, ini, des, qrcode_url)
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


@commodity_page.route('/commodity', methods=['GET'])
def query_commodity():
    commodities = Commodity.query.all()
    data = []
    for commodity in commodities:
        data.append({
            'user_id': commodity.user_id,
            'area_id': commodity.area_id,
            'batch': commodity.batch,
            'name': commodity.name,
            'price': commodity.price,
            'weight': commodity.weight,
            'logistics_id': commodity.logistics_id,
            'ini': commodity.ini,
            'des': commodity.des,
            'qrcode_url': commodity.qrcode_url
        })
    return jsonify(data)


'''
查询指定id商品信息
'''


@commodity_page.route('/commodity/<logistics_id>', methods=['GET'])
def get_commodity(logistics_id):
    commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
    if commodity:
        return jsonify({
            'user_id': commodity.user_id,
            'area_id': commodity.area_id,
            'batch': commodity.batch,
            'name': commodity.name,
            'price': commodity.price,
            'weight': commodity.weight,
            'logistics_id': commodity.logistics_id,
            'ini': commodity.ini,
            'des': commodity.des,
            'qrcode_url': commodity.qrcode_url
        })
    else:
        return '商品不存在'


'''
获取二维码图片
'''


@commodity_page.route('/commodity/img/<logistics_id>', methods=['GET'])
def get_img(logistics_id):
    img_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/qr_codes/'+logistics_id+'.png'
    return send_file(img_path, mimetype='image/gif')


