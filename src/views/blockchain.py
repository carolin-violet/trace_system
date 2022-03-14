"""
区块链api模块
"""
from flask import Blueprint, jsonify, request
from src.models import Blockchain, db, Logistics, Commodity
from src.utils import chain
from src.security import RSA


chain_page = Blueprint('chain_page', __name__)


'''
增加一个区块
'''


@chain_page.route('/blockchain', methods=['POST'])
def add_block():
    logistics_id = request.json['logistics_id']
    summary = {}

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
    汇总存储信息
    '''

    '''
    汇总生产信息
    '''


    blocks = Blockchain.query.all()
    blockchain = chain.Chain(blocks, db)

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
def validate_chain(commodity_id):
    blocks = Blockchain.query.all()
    verify_chain = chain.Chain(commodity_id, blocks)
    is_correct = verify_chain.validate_chain
    if is_correct:
        return 'true'  # 区块链正确
    else:
        return 'false'   # 区块链中有错
