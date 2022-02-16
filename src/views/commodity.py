"""
商品信息模块
"""
from src.models import Commodity
from flask import Blueprint

commodity_page = Blueprint('commodity_page', __name__)


# 添加商品信息
@commodity_page.route('/commodity', methods=['POST'])
def add_commodity():
    pass


# 删除商品信息
@commodity_page.route('/commodity/<product_id>', methods=['DELETE'])
def del_commodity(product_id):
    pass


# 查询所有商品信息
@commodity_page.route('/commodity', methods=['GET'])
def query_commodity():
    pass


# 查询指定id商品信息
@commodity_page.route('/commodity/<product_id>', methods=['GET'])
def get_commodity(product_id):
    pass


# 修改商品信息
@commodity_page.route('/commodity/<product_id>', methods=['PATCH'])
def modify_commodity(product_id):
    pass
