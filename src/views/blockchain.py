"""
区块链api模块
"""
from src.models import Blockchain, db
from src.utils import chain
from flask import Blueprint, jsonify
import json


chain_page = Blueprint('chain_page', __name__)


'''
查询一共有多少条区块链
每条链作为一组数据
'''


@chain_page.route('/chains/count', methods=['GET'])
def query_count():
    chains = Blockchain.query.group_by(Blockchain.commodity_id).count()
    return str(chains)


'''
查询一条区块链信息
'''


@chain_page.route('/chains/<commodity_id>', methods=['GET'])
def query_chain(commodity_id):
    blocks = Blockchain.query.filter(Blockchain.commodity_id == commodity_id).all()

    data_1 = json.loads(blocks[1].data, strict=False)
    # print(data_1)
    data = {
        "商品id": commodity_id,
        "始发地": data_1["ini"],
        "目的地": data_1["des"],
        "运输信息": []
    }
    for block in blocks:
        if block.index != 0:
            detail_data = json.loads(block.data, strict=False)
            data['运输信息'].append({
                "时间": detail_data["time"],
                "状态": detail_data["status"],
                "操作公司": detail_data["com"],
                "当前所在地": detail_data["cur"],
                "操作人": detail_data["person"],
                "操作人电话": detail_data["tel"]
            })
    return jsonify(data)


'''
验证一条区块链的合理性
'''


@chain_page.route('/chains/validate_proof/<commodity_id>', methods=['GET'])
def validate_chain(commodity_id):
    blocks = Blockchain.query.filter(Blockchain.commodity_id == commodity_id).all()
    verify_chain = chain.Chain(commodity_id, blocks)
    is_correct = verify_chain.validate_chain
    if is_correct:
        return 'true'  # 区块链正确
    else:
        return 'false'   # 区块链中有错
