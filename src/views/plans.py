"""
计划模块
"""
from src.models import Plan, db
from flask import Blueprint, request

api = Blueprint('plans', __name__)


# 添加一个计划
@api.route('/plans', methods=['POST'])
def addPlan():
    startTime = request.json['startTime']
    endTime = request.json['endTime']
    content = request.json['content']
    completed = request.json['completed']

    plan = Plan(startTime=startTime, endTime=endTime, content=content, completed=completed)
    db.session.add(plan)
    db.session.commit()
    return {
        "msg": "添加成功"
    }


# 查询当天未完成的计划
@api.route('/plans', methods=['GET'])
def getPlans():
    date = request.args.get('date')
    plans = []  # 存放当前日期的计划
    all_plan = Plan.query.all()
    for plan in all_plan:
        if str(plan.startTime).startswith(date) & str(plan.startTime).startswith(date) &(plan.completed == 0):
            plans.append({
                "id": plan.id,
                "startTime": str(plan.startTime.time()),
                "endTime": str(plan.endTime.time()),
                "content": plan.content,
                "completed": plan.completed
            })
    return {
        "msg": "查询成功",
        "plans": plans
    }


# 修改当天的计划完成信息
@api.route('/plans/update', methods=['POST'])
def updatePlans():
    for plan in request.json['data']:
        if plan:
            p = Plan.query.filter(Plan.id == plan['id']).first()
            p.completed = plan['completed']
    db.session.commit()
    return {
        "msg": "更新成功"
    }



