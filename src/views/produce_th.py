"""
生产过程温湿度信息
"""
from flask import Blueprint, request, jsonify
import time
from src.models import ProduceTH, db

produce_th_page = Blueprint('produce_th_page', __name__)

'''
添加温度信息
'''


@produce_th_page.route('/produce_th', methods=['POST'])
def add_produce_th():
    user_id = request.json['user_id']
    area_id = request.json['area_id']
    batch = request.json['batch']
    temp = request.json['temp']
    hum = request.json['hum']
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    th = ProduceTH(user_id, area_id, batch, temp, hum, date)
    db.session.add(th)
    db.session.commit()

    return '添加成功'


'''
查询指定产商指定区域农作物的温湿度
'''


@produce_th_page.route('/produce_th/<producer_id>/<area_id>', methods=['GET'])
def query_produce_th(producer_id, area_id):
    information = ProduceTH.query.filter((ProduceTH.user_id == producer_id) & (ProduceTH.area_id == area_id)).all()

    data = []
    for info in information:
        data.append({
            "batch": info.batch,
            "temp": info.temp,
            "hum": info.hum,
            "date": info.date
        })
    return jsonify(data)
