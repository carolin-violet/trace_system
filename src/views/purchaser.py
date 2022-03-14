"""
区块链api模块
"""
from flask import Blueprint, jsonify, request
from src.models import Blockchain, db, Logistics, Commodity, ProduceTH, Produce, Purchase, User
from src.utils import chain
from src.security import RSA


purchaser_page = Blueprint('purchaser_page', __name__)


'''
顾客查询自己的所有购买信息
'''


@purchaser_page.route('/purchase', methods=['GET'])
def add_block():


