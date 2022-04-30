"""
区块链api模块
"""

from flask import Blueprint, render_template, send_file, jsonify, request
import os
from src.models import User, Blockchain, Commodity
from src.security import RSA, token_auth

sale_page = Blueprint('sale_page', __name__)


'''
查看销售商销售的商品
'''


@sale_page.route('/commodities/<saler_id>', methods=['GET'])
def get_commodity(saler_id):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'admin' or 'saler':
        pass
    else:
        return '权限不够'

    commodities = Commodity.query.filter(Commodity.saler_id == saler_id).all()
    data = []
    for commodity in commodities:
        data.append({
            'producer_id': commodity.producer_id,
            'area_id': commodity.area_id,
            'batch': commodity.batch,
            'name': commodity.name,
            'weight': commodity.weight,
            'logistics_id': commodity.logistics_id,
            'ini': commodity.ini,
            'des': commodity.des,
            'qrcode_url': commodity.qrcode_url
        })
    return jsonify(data)


'''
获取二维码图片
'''


@sale_page.route('/commodity/qrcode_img/<logistics_id>', methods=['GET'])
def get_qrcode(logistics_id):
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if role == 'admin' or 'saler':
        pass
    else:
        return '权限不够'
    img_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/qr_codes/'+logistics_id+'.png'
    return send_file(img_path, mimetype='image/gif')


'''
扫了二维码后跳转指定页面
'''


@sale_page.route('/commodity/detail/<logistics_id>/<saler_id>', methods=['GET'])
def query_detail(logistics_id, saler_id):

    print(logistics_id, saler_id)

    block = Blockchain.query.filter(Blockchain.logistics_id == logistics_id).first()

    # 获取私钥
    private_key = User.query.filter(User.user_id == saler_id).first().private_key

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

    # 将数据中的图片地址切换成图片src
    for i in range(0, len(message['produce_data'])):
        with open(message['produce_data'][i]['img_path'], 'r') as fp:
            message['produce_data'][i]['img_path'] = fp.read()

    return render_template('detail.html', data=message)


