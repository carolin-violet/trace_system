"""
存储信息
"""
from src.models import Store, db
from flask import Blueprint, request, jsonify

store_page = Blueprint('store_page', __name__)

'''
添加存储信息
'''


@store_page.route('/store', methods=['POST'])
def add_store_info():
    user_id = request.form['user_id']
    area_id = request.form['area_id']
    batch = request.form['batch']
    repository_index = request.form['repository_index']
    in_time = request.form['in_time']
    out_time = request.form['out_time']
    description = request.form['description']
    img_path = request.form['img_path']

    store_info = Store(user_id, area_id, batch, repository_index, in_time, out_time, description, img_path)
    db.session.add(store_info)
    db.session.commit()


'''
查询指定产商的存储信息
'''


@store_page.route('/store/<producer_id>', methods=['GET'])
def query_store_info(producer_id):
    information = Store.query.filter(Store.user_id == producer_id).all()
    if not information:
        return "无存储"
    data = []
    for info in information:
        data.append({
            "area_id": info.area_id,
            "batch": info.batch,
            "repository_index": info.repository_index,
            "in_time": info.in_time,
            "out_time": info.out_time,
            "description": info.description,
            "img_path": info.img_path
        })
    return jsonify(data)


