"""
存储过程温湿度信息
"""
from flask import Blueprint, request, jsonify
import time
from src.models import StoreTH, db

store_th_page = Blueprint('store_th_page', __name__)

'''
添加存储温湿度信息
'''


@store_th_page.route('/store_th', methods=['POST'])
def add_produce_th():
    user_id = request.json['user_id']
    area_id = request.json['area_id']
    batch = request.json['batch']
    repository_index = request.json['repository_index']
    temp = request.json['temp']
    hum = request.json['hum']
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    th = StoreTH(user_id, area_id, batch, repository_index, temp, hum, date)
    db.session.add(th)
    db.session.commit()


'''
查询指定产商指定区域农作物的存储温湿度
'''


@store_th_page.route('/store_th/<producer_id>/<area_id>', methods=['GET'])
def query_produce_th(producer_id, area_id):
    information = StoreTH.query.filter((StoreTH.user_id == producer_id) & (StoreTH.area_id == area_id)).all()

    data = []
    for info in information:
        data.append({
            "batch": info.batch,
            "repository_index": info.repository_index,
            "temp": info.temp,
            "hum": info.hum,
            "date": info.date
        })
    return jsonify(data)
