from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''数据库模型'''


# 用户基本信息表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id作为用户id
    nickName = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), unique=True)  # 手机号码,用作登录账号,用作主键
    password = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(6), nullable=False)  # 性别:male/female
    email = db.Column(db.String(20), nullable=False)  # 电子邮箱


# 文章信息表
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)  # id
    article_id = db.Column(db.Integer, nullable=False)  # 文章id
    title = db.Column(db.String(30), nullable=False)  # 标题
    author = db.Column(db.String(20), nullable=False)  # 作者
    paragraph_id = db.Column(db.Integer, nullable=False)  # 段落
    content = db.Column(db.Text, nullable=False)  # 内容


# 计划信息表
class Plan(db.Model):
    __tablename__ = "plans"
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)  # id
    startTime = db.Column(db.DateTime, nullable=False)  # 开始时间
    endTime = db.Column(db.DateTime, nullable=False)  # 截止时间
    content = db.Column(db.String(50), nullable=False)  # 内容
    completed = db.Column(db.Integer, default=0)  # 完成情况


# 笔记信息表
class Diary(db.Model):
    __tablename__ = "diaries"
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)  # id
    date = db.Column(db.DateTime, nullable=False)  # 日期
    content = db.Column(db.Text, nullable=False)  # 内容


# 导航信息表
class Navigation(db.Model):
    __tablename__ = "navigations"
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)  # id
    category = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), default="")
