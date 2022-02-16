"""
物流信息模块
"""
from src.models import Logistics
from flask import Blueprint

logistics_page = Blueprint('logistics_page', __name__)


# 添加物流信息
@logistics_page.route('/logistics', methods=['POST'])
def add_logistics():
    pass


# 删除物流信息
@logistics_page.route('/logistics/<product_id>', methods=['DELETE'])
def del_logistics(product_id):
    pass


# 修改物流信息
@logistics_page.route('/logistics/<product_id>', methods=['PATCH'])
def modify_logistics(product_id):
    pass


# 查询物流信息
@logistics_page.route('/logistics/<product_id>', methods=['GET'])
def query_logistics(product_id):
    pass

