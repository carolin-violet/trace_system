"""
商品信息模块
"""
from src.models import Commodity, db
from flask import Blueprint, request, jsonify
from uuid import uuid1

commodity_page = Blueprint('commodity_page', __name__)


# 添加商品信息
@commodity_page.route('/commodity', methods=['POST'])
def add_commodity():
    name = request.form['name']
    price = request.form['price']
    weight = request.form['weight']
    total = request.form['total']
    user_id = request.form['user_id']
    product_id = uuid1()
    commodity = Commodity(name, price, weight, total, product_id, user_id)
    db.session.add(commodity)
    db.session.commit()

    return '添加成功'


# 删除商品信息
@commodity_page.route('/commodity/<product_id>', methods=['DELETE'])
def del_commodity(product_id):
    commodity = Commodity.query.filter(Commodity.product_id == product_id).first()
    if commodity:
        db.session.delete(commodity)
        db.session.commit()
        return '删除成功'
    else:
        return '商品不存在'


# 查询所有商品信息
@commodity_page.route('/commodity', methods=['GET'])
def query_commodity():
    commodities = Commodity.query.all()
    data = []
    for commodity in commodities:
        data.append({
            'product_id': commodity.product_id,
            'user_id': commodity.user_id,
            'name': commodity.name,
            'price': commodity.price,
            'weight': commodity.weight,
            'total': commodity.total,
        })
    return jsonify(data)


# 查询指定id商品信息
@commodity_page.route('/commodity/<product_id>', methods=['GET'])
def get_commodity(product_id):
    commodity = Commodity.query.filter(Commodity.product_id == product_id).first()
    if commodity:
        return jsonify({
            'product_id': commodity.product_id,
            'user_id': commodity.user_id,
            'name': commodity.name,
            'price': commodity.price,
            'weight': commodity.weight,
            'total': commodity.total,
        })
    else:
        return '商品不存在'


'''
获取二维码图片
'''


@commodity_page.route('/commodity/img/<product_id>', methods=['GET'])
def get_img(product_id):
    pass