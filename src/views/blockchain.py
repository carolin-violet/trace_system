"""
区块链api模块
"""
from flask import Blueprint, jsonify, request
from src.models import Blockchain, db, Logistics, Commodity, ProduceTH, Produce, Purchase, User
from src.utils import chain
from src.security import RSA


chain_page = Blueprint('chain_page', __name__)


'''
增加一个区块
'''


@chain_page.route('/blockchain', methods=['POST'])
def add_block():
    logistics_id = request.json['logistics_id']

    '''
    汇总物流信息
    '''
    logistics_s = Logistics.query.filter(Logistics.logistics_id == logistics_id).all()
    logistics_data = []
    for lgs in logistics_s:
        logistics_data.append({
            "status": lgs.status,
            "com": lgs.com,
            "time": lgs.time,
            "cur": lgs.cur,
            "person": lgs.person,
            "tel": lgs.tel,
        })

    '''
    汇总商品信息
    '''
    commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
    commodity_data = {
        "user_id": commodity.user_id,
        "area_id": commodity.area_id,
        "batch": commodity.batch,
        "name": commodity.name,
        "price": commodity.price,
        "weight": commodity.weight,
        "logistics_id": commodity.logistics_id,
        "ini": commodity.ini,
        "des": commodity.des,
        "qrcode_url": commodity.qrcode_url
    }

    '''
    汇总发货前的生产信息
    '''
    th_data = []
    produce_data = []
    ths = ProduceTH.query.filter((ProduceTH.user_id == commodity.user_id) & (ProduceTH.area_id == commodity.area_id) & (ProduceTH.batch == commodity.batch)).all()
    for th in ths:
        th_data.append({
            "temp": th.temp,
            "hum": th.hum,
            "date": th.date,
        })
    produces = Produce.query.filter((Produce.user_id == commodity.user_id) & (Produce.area_id == commodity.area_id) & (Produce.batch == commodity.batch)).all()
    for produce in produces:
        produce_data.append({
            "op_type": produce.op_type,
            "op_time": produce.op_time,
            "description": produce.description,
            "img_path": produce.img_path,
        })

    '''
    汇总数据并加密
    '''
    summary = {
        'commodity_data': commodity_data,
        'produce_data': produce_data,
        'th_data': th_data,
        'logistics_data': logistics_data
    }

    purchaser = Purchase.query.filter(Purchase.logistics_id == logistics_id).first()
    purchaser_id = purchaser.user_id

    public_key = RSA.normalize_keys(User.query.filter(User.user_id == purchaser_id).first().public_key)
    print(public_key)
    print(type(summary))
    data = RSA.encrypt(summary, public_key)

    '''
    添加区块
    '''
    blocks = Blockchain.query.all()
    blockchain = chain.Chain(blocks, db)
    blockchain.new_block(logistics_id, data)

    return '添加成功'


'''
查询整条区块链信息
'''


@chain_page.route('/blockchain', methods=['GET'])
def query_chain():
    blocks = Blockchain.query.all()

    data = []
    for block in blocks:
        data.append({
            "logistics_id": block.logistics_id,
            "cur_hash": block.cur_hash,
            "pre_hash": block.pre_hash,
            "timestamp": block.timestamp,
            "nonce": block.nonce,
            "data": block.data,
        })
    return jsonify(data)


'''
验证区块链的合理性
'''


@chain_page.route('/blockchain/validate_proof', methods=['GET'])
def validate_chain():
    blocks = Blockchain.query.all()
    blockchain = chain.Chain(blocks, db)
    is_correct = blockchain.validate_chain()
    if is_correct:
        return 'true'  # 区块链正确
    else:
        return 'false'   # 区块链中有错

