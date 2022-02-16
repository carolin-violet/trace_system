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


# 查询物流信息
@logistics_page.route('/logistics/<product_id>', methods=['GET'])
def query_logistics(product_id):
    pass


# 修改物流状态
@logistics_page.route('/logistics/status/<product_id>', methods=['PATCH'])
def modify_logistics_status(product_id):
    pass


# 修改物流当前所在地
@logistics_page.route('/logistics/cur/<product_id>', methods=['PATCH'])
def modify_logistics_cur(product_id):
    pass


# 修改物流操作信息(包含操作公司，操作时间，操作人，操作人联系方式)
@logistics_page.route('/logistics/op/<product_id>', methods=['PATCH'])
def modify_logistics_op(product_id):
    pass
