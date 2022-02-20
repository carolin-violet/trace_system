"""
区块链api模块
"""
from src.models import Blockchain
from src.utils import chain
from flask import Blueprint, jsonify

chain_page = Blueprint('chain_page', __name__)


'''
查询所有区块链信息
每条链作为一组数据
'''


@chain_page.route('/chains', methods=['GET'])
def query_chains():
    pass


'''
查询一条区块链信息
'''


@chain_page.route('/chains/<commodity_id>', methods=['GET'])
def query_chain(commodity_id):
    blocks = Blockchain.query.filter(Blockchain.commodity_id == commodity_id).all()
    data = {
        "商品id": blocks[0].commodity_id,
        "始发地": blocks[0].ini,
        "目的地": blocks[0].des,
        "运输信息": []
    }
    for block in blocks:
        data['运输信息'].append({
            "时间": block.time,
            "状态": block.status,
            "操作公司": block.com,
            "当前所在地": block.cur,
            "操作人": block.person,
            "操作人电话": block.tel
        })
    return jsonify(data)


'''
验证一条区块链的合理性
'''


@chain_page.route('/chains/validate_proof/<commodity_id>', methods=['GET'])
def validate_chain(commodity_id):
    verify_chain = chain.Chain(commodity_id)
    is_correct = verify_chain.validate_chain()
    if is_correct:
        return 'true'  # 区块链正确
    else:
        return 'false'   # 区块链中有错
