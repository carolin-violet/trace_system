"""
生产信息
"""
from flask import Blueprint, request, jsonify
import time
import os
from src.models import Produce, db

produce_page = Blueprint('produce_page', __name__)

'''
添加生产信息
'''


@produce_page.route('/produce', methods=['POST'])
def add_produce_info():
    user_id = request.form['user_id']
    area_id = request.form['area_id']
    batch = request.form['batch']
    op_type = request.form['op_type']
    op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    description = request.form['description']

    '''
    接收并保存图片
    '''
    img = request.files.get('photo')
    rel_path = user_id + '--' + area_id + '--' + batch + '--' + op_type + '--' + op_time.split(' ')[0] + '.' + img.filename.split('.')[-1]
    img_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/produce_img/' + rel_path
    img.save(img_path)

    produce_info = Produce(user_id, area_id, batch, op_type, op_time, description, img_path)
    db.session.add(produce_info)
    db.session.commit()

    return '添加成功'


'''
查询指定产商的生产信息
'''


@produce_page.route('/produce/<producer_id>', methods=['GET'])
def query_produce_info(producer_id):
    information = Produce.query.filter(Produce.user_id == producer_id).all()
    if not information:
        return "无生产信息"
    data = []
    for info in information:
        data.append({
            "area_id": info.area_id,
            "batch": info.batch,
            "op_type": info.op_type,
            "op_time": info.op_time,
            "description": info.description,
            "img_path": info.img_path,
        })
    return jsonify(data)


