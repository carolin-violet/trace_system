"""
登录模块
"""
import json

from src.models import Navigation
from flask import Blueprint

api = Blueprint('navigation', __name__)


@api.route('/navigations', methods=['GET'])
def getNavs():
    navigations = Navigation.query.all()
    navs = [
        {"category_id": 1, "title": '学习导航', "content": []},
        {"category_id": 2, "title": '软件工具', "content": []},
        {"category_id": 3, "title": 'web开发', "content": []},
        {"category_id": 4, "title": '素材渠道', "content": []},
        {"category_id": 5, "title": '动漫影视音乐', "content": []},
        {"category_id": 6, "title": '网盘存储', "content": []},
        {"category_id": 7, "title": '收藏博客', "content": []}
    ]
    for nav in navigations:
        navs[nav.category_id-1]['content'].append({
           "id": nav.id,
           "title": nav.title,
           "url": nav.url,
           "img_url": nav.img_url
        })
    return {
        "msg": "获取成功",
        "navigations": navs
    }






