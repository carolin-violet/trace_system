"""
区块链api模块
"""

from flask import Blueprint, jsonify, request, render_template
from src.models import Purchase, db, User, Blockchain
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


@purchase_page.route('/purchase/detail/<logistics_id>', methods=['GET'])
def query_detail(logistics_id):
    block = Blockchain.query.filter(Blockchain.logistics_id == logistics_id).first()

    # 获取私钥
    purchaser_id = Purchase.query.filter(Purchase.logistics_id == logistics_id).first().user_id
    private_key = User.query.filter(User.user_id == purchaser_id).first().private_key

    # 解密区块链中的加密数据
    cipher_path = block.data_path
    with open(cipher_path, 'rb') as fp:
        cipher = fp.read()
        i = 0
        cipher_list = []
        while i < len(cipher):
            cipher_list.append(cipher[i:i+64])
            i += 64
    message = RSA.decrypt(cipher_list, private_key)

    return render_template('detail.html', data=message)

