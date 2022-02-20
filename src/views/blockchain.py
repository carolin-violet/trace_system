"""
区块链api模块
"""
from src.models import Blockchain, db
from src.utils import chain
from flask import Blueprint, request

chain_page = Blueprint('chain_page', __name__)


'''
查询所有区块链信息
'''


@chain_page.route('/chains', methods=['GET'])
def query_chains():
    pass


'''
查询一条区块链信息
'''


@chain_page.route('/chains/<commodity_id>', methods=['GET'])
def query_chain(commodity_id):
    pass


'''
验证一条区块链的合理性
'''
@chain_page.route('/chains/validate_proof/<commodity_id>', methods=['GET'])
def validate_chain(commodity_id):
    pass