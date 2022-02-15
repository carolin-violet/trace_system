"""
文章模块
"""
from flask import Blueprint, request
from src.models import db, Article
from utils.getArticle import get

api = Blueprint('articles', __name__)


# 随机爬一篇文章
@api.route('/articles/random', methods=['GET'])
def getArticleRandom():
    article = get()
    return article


# 数据库获取一篇文章
@api.route('/articles/<article_id>', methods=['GET'])
def getArticle(article_id):
    records = Article.query.filter(Article.article_id == article_id).all()
    if records:
        article = ({
            "article_id": records[0].article_id,
            "title": records[0].title,
            "author": records[0].author,
            "content": [p.content for p in records]
        })
        return {
                "msg": "获取成功",
                "article": article
            }
    else:
        return {
            "msg": "不存在此文章"
        }


# 获取所有文章数据
@api.route('/articles', methods=['GET'])
def getArticles():
    articles = Article.query.all()
    if articles:
        article_list = []
        unique_id = 0
        for p in articles:
            if p.article_id != unique_id:
                unique_id = p.article_id
                article_list.append({
                    "article_id": p.article_id,
                    "title": p.title,
                    "author": p.author,
                })
        return {
            "msg": "获取成功",
            "articles": article_list
        }
    else:
        return {
            "msg": "数据库无文章"
        }


# 添加一篇文章
@api.route('/articles', methods=['POST'])
def addArticle():
    title = request.json['title']
    author = request.json['author']
    content = request.json['content']

    article = Article.query.filter(Article.title == title, Article.author == author).first()
    if article:
        article_id = article.article_id
        return {
            "article_id": article_id,
            "msg": "此文章已存在"
        }
    else:
        articles = Article.query.all()
        if articles:
            article_count = max([i.article_id for i in articles])
            article_id = article_count + 1
        else:
            article_id = 1

        paragraph_id = 1
        for p in content:
            paragraph = Article(article_id=article_id, title=title, author=author, paragraph_id=paragraph_id, content=p)
            db.session.add(paragraph)
            db.session.commit()
            paragraph_id += 1
        return {
            "article_id": article_id,
            "msg": "添加成功"
        }


#删除一篇文章
@api.route('/articles/<article_id>', methods=['DELETE'])
def delArticle(article_id):
    article = Article.query.filter(Article.article_id == article_id).all()
    if article:
        for p in article:
            db.session.delete(p)
            db.session.commit()
        return {
            "msg": '删除成功'
        }
    else:
        return {
            "msg": "不存在此文章"
        }

