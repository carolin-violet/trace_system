"""
区块链api模块
"""

from flask import Blueprint, jsonify, request
from src.models import Blockchain, db, Logistics, Commodity, TH, Produce, User
from src.utils import chain
from src.security import RSA, token_auth


chain_page = Blueprint('chain_page', __name__)


'''
增加一个区块
当物流到达销售商的时候添加
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
            'transporter_id': lgs.transporter_id,
            'time': lgs.time,
            'status': lgs.status,
            'cur': lgs.cur
        })

    '''
    汇总商品信息
    '''
    commodity = Commodity.query.filter(Commodity.logistics_id == logistics_id).first()
    commodity_data = {
        'producer_id': commodity.producer_id,
        'area_id': commodity.area_id,
        'batch': commodity.batch,
        'name': commodity.name,
        'weight': commodity.weight,
        'saler_id': commodity.saler_id,
        'logistics_id': commodity.logistics_id,
        'ini': commodity.ini,
        'des': commodity.des,
        'qrcode_url': commodity.qrcode_url
    }

    '''
    汇总发货前的生产信息
    '''
    th_data = []
    produce_data = []
    ths = TH.query.filter((TH.user_id == commodity.producer_id) & (TH.area_id == commodity.area_id) & (TH.batch == commodity.batch)).all()
    for th in ths:
        th_data.append({
            "temp": th.temp,
            "hum": th.hum,
            "time": th.time,
        })
    produces = Produce.query.filter((Produce.producer_id == commodity.producer_id) & (Produce.area_id == commodity.area_id) & (Produce.batch == commodity.batch)).all()
    for produce in produces:
        produce_data.append({
            "op_type": produce.op_type,
            "op_time": produce.op_time,
            "description": produce.description,
            "img": produce.img,
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

    public_key = User.query.filter(User.user_id == commodity.saler_id).first().public_key
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
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    blocks = Blockchain.query.all()
    data = []

    for block in blocks:
        data.append({
            "logistics_id": block.logistics_id,
            "cur_hash": block.cur_hash,
            "pre_hash": block.pre_hash,
            "timestamp": block.timestamp,
            "nonce": block.nonce,
            "data_path": block.data_path,
        })
    return jsonify(data)


'''
查询不在区块链中的商品信息(运输状态为已到货)
'''


@chain_page.route('/blockchain/out-chain', methods=['GET'])
def query_out_chain():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    out_chain_commodity = []
    commodities = Commodity.query.all()
    for commodity in commodities:
        commodity_status = Logistics.query.filter(Logistics.logistics_id == commodity.logistics_id).all()[-1].status
        is_in_chain = Blockchain.query.filter(Blockchain.logistics_id == commodity.logistics_id).first()
        if (commodity_status == '已到货') & (not is_in_chain):
            out_chain_commodity.append({
                "logistics_id": commodity.logistics_id
            })
    return jsonify(out_chain_commodity)


'''
验证区块链的合理性
'''


@chain_page.route('/blockchain/validate_proof', methods=['GET'])
def validate_chain():
    token_data = token_auth.verify_token(request.headers['Authorization'])
    if token_data == 'token过期或错误':
        return '请重新登录'

    blocks = Blockchain.query.all()
    blockchain = chain.Chain(blocks, db)
    is_correct = blockchain.validate_chain()
    if is_correct:
        return {
            "code": 0,
            "msg": 'true'
        }  # 区块链正确
    else:
        return {
            "code": 1,
            "msg": 'error'
        }   # 区块链中有错

