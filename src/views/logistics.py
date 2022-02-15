"""
物流信息模块
"""
# from src.models import Logistics
from flask import Blueprint

logistics_page = Blueprint('logistics_page', __name__)


@logistics_page.route('/logistics', methods=['POST'])
def logistics():
    pass
