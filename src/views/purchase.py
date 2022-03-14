"""
区块链api模块
"""

from flask import Blueprint, jsonify, request
from src.models import Purchase, db

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



