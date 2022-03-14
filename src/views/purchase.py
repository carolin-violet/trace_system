"""
区块链api模块
"""
import json

from flask import Blueprint, jsonify, render_template
from src.models import Purchase, Blockchain, User
from src.security import RSA

purchase_page = Blueprint('purchase_page', __name__)


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
    cipher_data = block.data

    user_id = Purchase.query.filter(Purchase.logistics_id == logistics_id).first().user_id
    private_key = User.query.filter(User.user_id == user_id).first().private_key

    data = json.loads(RSA.decrypt(cipher_data, RSA.normalize_keys(private_key)))
    return render_template('show_data.html', data=data)

