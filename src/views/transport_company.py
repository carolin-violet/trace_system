"""
商品信息模块
"""
from flask import Blueprint, request, jsonify
from src.models import TransportCmp, db
from src.security import token_auth

transport_company_page = Blueprint('transport_company_page', __name__)


'''
添加运输公司信息
'''


@transport_company_page.route('/transport_company', methods=['POST'])
def add_company_info():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = TransportCmp.query.filter(TransportCmp.staff_id == token_data['user_id']).first().role
    if (token_data['user_id'] == '0') | (role == 'manager'):
        company_name = request.json['company_name']
        staff_id = request.json['staff_role']
        staff_role = request.json['staff_role']
        staff_name = request.json['staff_name']
        staff_tel = request.json['staff_tel']

        transport_company_info = TransportCmp(company_name, staff_id, staff_role, staff_name, staff_tel)
        db.session.add(transport_company_info)
        db.session.commit()
        return '添加成功'
    else:
        return '无权限'


'''
删除公司
'''


@transport_company_page.route('/transport_company/<company_name>', methods=['DELETE'])
def del_staff(company_name):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        companies = TransportCmp.query.filter(TransportCmp.company_name == company_name).all()
        if companies:
            db.session.delete(companies)
            db.session.commit()
            return '删除成功'
        else:
            return '不存在此公司'
    else:
        return '无权限'


'''
删除员工
'''


@transport_company_page.route('/transport_company/<staff_id>', methods=['DELETE'])
def del_staff(staff_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = TransportCmp.query.filter(TransportCmp.staff_id == token_data['user_id']).first().role
    if (token_data['user_id'] == '0') | (role == 'manager'):
        staff = TransportCmp.query.filter(TransportCmp.staff_id == staff_id).first()
        if staff:
            db.session.delete(staff)
            db.session.commit()
        else:
            return '不存在此员工'
    else:
        return '无权限'


'''
修改公司信息,主要修改管理员姓名与电话号
'''


@transport_company_page.route('/transport_company/info/<manager_id>', methods=['PATCH'])
def update_company_info(manager_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    company = TransportCmp.query.filter(TransportCmp.staff_id == manager_id).first()
    if company:
        if (token_data['user_id'] == '0') | (company.staff_role == 'manager'):
            manager_name = request.json['manager_name']
            manager_tel = request.json['manager_tel']
            company.staff_name = manager_name
            company.staff_tel = manager_tel
            db.session.commit()
            return '修改成功'
        else:
            return '无权限'
    else:
        return '不存在此公司'



'''
查询所有公司信息
'''


@transport_company_page.route('/transport_company', methods=['GET'])
def query_all_company():
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    if token_data['user_id'] == '0':
        information = TransportCmp.query.filter(TransportCmp.staff_role == 'manager').all()
        data = []
        for info in information:
            data.append({
                "company_name": info.company_name,
                "manager_id": info.staff_id,
                "manager_name": info.staff_name,
                "manager_tel": info.staff_tel
            })
        return jsonify(data)
    else:
        return '无权限'


'''
查询一个公司的所有信息
'''


@transport_company_page.route('/transport_company/<company_name>', methods=['GET'])
def query_company(company_name):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    role = TransportCmp.query.filter(TransportCmp.staff_id == token_data['user_id']).first().role
    if (token_data['user_id'] == '0') | (role == 'manager'):
        information = TransportCmp.query.filter(TransportCmp.company_name == company_name).all()
        data = []
        for info in information:
            data.append({
                "staff_id": info.staff_id,
                "staff_role": info.staff_role,
                "staff_name": info.staff_name,
                "staff_tel": info.staff_tel
            })
        return jsonify(data)
    else:
        return '无权限'


