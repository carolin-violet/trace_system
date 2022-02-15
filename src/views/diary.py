"""
日记模块
"""
from src.models import db, Diary
from flask import Blueprint, request

api = Blueprint('diary', __name__)


# 上传日记
@api.route('/diaries', methods=['POST'])
def addDiary():
    date = request.json['date']
    content = request.json['content']

    diary = Diary(date=date, content=content)
    db.session.add(diary)
    db.session.commit()
    return {
        "msg": "上传成功"
    }


# 获取日记的id和日期
@api.route('/diaries', methods=['GET'])
def getDiaries():
    diaries = Diary.query.all()
    diary_list = []
    for diary in diaries:
        diary_list.append({
            "id": diary.id,
            "date": str(diary.date)
        })
    return {
        "msg": "获取成功",
        "diaries": diary_list
    }


# 根据id获取日记的内容
@api.route('/diaries/<id>', methods=['GET'])
def getDiary(id):
    diary = Diary.query.filter(Diary.id == id).first()
    diary_content = {
        "id": diary.id,
        "date": str(diary.date),
        "content": diary.content,
    }
    return {
        "msg": "获取成功",
        "diary": diary_content
    }