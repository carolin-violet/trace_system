"""
生产过程温湿度信息
"""
from src.models import ProduceMonitor, db
from flask import Blueprint, request, jsonify

produce_monitor_page = Blueprint('produce_monitor_page', __name__)

'''
添加温度信息
'''


@produce_monitor_page.route('/', methods=['POST'])
def add_produce_info():



'''
查询指定产商的生产信息
'''


@produce_monitor_page.route('/produce/<producer_id>', methods=['GET'])
def query_produce_info(producer_id):



