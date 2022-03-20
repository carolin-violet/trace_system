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
    if token_data['user_id'] == '0':
        print(request.json)
        company_name = request.json['company_name']
        staff_id = request.json['staff_id']
        staff_role = request.json['staff_role']
        staff_name = request.json['staff_name']
        staff_tel = request.json['staff_tel']

        transport_company_info = TransportCmp(company_name, staff_id, staff_role, staff_name, staff_tel)
        db.session.add(transport_company_info)
        db.session.commit()
        return '成功'
    else:
        return '无权限'


'''
删除公司
'''


@transport_company_page.route('/transport_companies/<company_name>', methods=['DELETE'])
def del_company(company_name):
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
    if token_data['user_id'] == '0':
        staff = TransportCmp.query.filter(TransportCmp.staff_id == staff_id).first()
        if staff:
            db.session.delete(staff)
            db.session.commit()
            return '删除成功'
        else:
            return '不存在此员工'
    else:
        return '无权限'


'''
修改员工信息
'''


@transport_company_page.route('/transport_company/info/<staff_id>', methods=['PATCH'])
def update_company_info(staff_id):
    token_data = token_auth.verify_token(request.headers['token'])
    if token_data == 'token过期或错误':
        return '请重新登录'
    staff_info = TransportCmp.query.filter(TransportCmp.staff_id == staff_id).first()
    if staff_info:
        if token_data['user_id'] == '0':
            staff_info.staff_name = request.json['staff_name']
            staff_info.staff_tel = request.json['staff_tel']
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
    if token_data['user_id'] == '0':
        information = TransportCmp.query.filter(TransportCmp.company_name == company_name).all()
        data = []
        for info in information:
            if info.staff_role != 'manager':
                data.append({
                    "staff_id": info.staff_id,
                    "staff_name": info.staff_name,
                    "staff_tel": info.staff_tel
                })
        return jsonify(data)
    else:
        return '无权限'


