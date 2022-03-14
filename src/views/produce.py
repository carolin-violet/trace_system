"""
生产信息
"""
from src.models import Produce, db
from flask import Blueprint, request, jsonify

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
    op_time = request.form['op_time']
    description = request.form['description']

    produce_info = Produce(user_id, area_id, batch, op_type, op_time, description)
    db.session.add(produce_info)
    db.session.commit()


'''
添加生产过程拍摄的图片
'''


@produce_page.route('/produce/img', methods=['POST'])
def add_produce_image():
    pass


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


