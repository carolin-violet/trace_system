"""
区块链api模块
"""
import json

from flask import Blueprint, jsonify, render_template, request
from src.models import Purchase, Blockchain, User, db
from src.security import RSA

purchase_page = Blueprint('purchase_page', __name__)


'''
添加购买信息
'''


@purchase_page.route('/purchase', methods=['POST'])
def add_purchase():
    user_id = request.json['user_id']
    logistics_id = request.json['logistics_id']
    purchases = Purchase(user_id, logistics_id)

    db.session.add(purchases)
    db.session.commit()

    return '添加成功'


'''
指定顾客查询自己的所有购买商品
'''


@purchase_page.route('/purchase/<user_id>', methods=['GET'])
def query_purchase(user_id):
    purchases = Purchase.query.filter(Purchase.user_id == user_id).all()
    data = []
    for purchase in purchases:
        data.append(purchase.logistics_id)
    return jsonify(data)


'''
扫了二维码后跳转指定页面
'''


@purchase_page.route('/purchase/<logistics_id>', methods=['GET'])
def get_img(logistics_id):
    block = Blockchain.query.filter(Blockchain.logistics_id == logistics_id).first()
    return render_template('show_data.html', data=block.data)

