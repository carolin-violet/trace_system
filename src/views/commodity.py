"""
商品信息模块
"""
from src.models import Commodity
from flask import Blueprint, request

commodity_page = Blueprint('commodity_page', __name__)


@commodity_page.route('/commodity', methods=['POST'])
def commodity():
    pass


