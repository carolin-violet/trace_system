"""
登录模块
"""
from src.models import Produce
from flask import Blueprint, request

produce_page = Blueprint('produce_page', __name__)


@produce_page.route('/produce', methods=['POST'])
def add_produce_info():




