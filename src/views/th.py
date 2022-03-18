"""
生产过程温湿度信息
"""
from flask import Blueprint, request, jsonify
import time
from src.security import token_auth
from src.models import TH, db, User

th_page = Blueprint('th_page', __name__)

'''
添加温度信息
'''


@th_page.route('/produce_th', methods=['POST'])
def add_produce_th():
    user_id = request.json['user_id']
    area_id = request.json['area_id']
    batch = request.json['batch']
    temp = request.json['temp']
    hum = request.json['hum']
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    th = TH(user_id, area_id, batch, temp, hum, date)
    db.session.add(th)
    db.session.commit()

    return '添加成功'


'''
查询指定产商农作物的温湿度
'''


@th_page.route('/produce_th/<producer_id>', methods=['GET'])
def query_produce_th(producer_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = User.query.filter(User.user_id == token_data['user_id']).first().role
    if (role == 'producer' or 'admin') & (token_data['user_id'] == producer_id or '0'):
        information = TH.query.filter(TH.user_id == producer_id).all()

        data = []
        for info in information:
            data.append({
                "batch": info.batch,
                "temp": info.temp,
                "hum": info.hum,
                "date": info.date
            })
        return jsonify(data)
    else:
        return '无权限'
