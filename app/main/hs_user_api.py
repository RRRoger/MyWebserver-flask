# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, url_for
from . import main
from ..models import User, Post
from flask import render_template, session
from flask_login import login_user, logout_user, login_required
from .hs_user_forms import HsUserSearch, HsUserForm, HsUserResetPasswordForm
from ..models import User, Role
from flask import Flask
from .. import db
from sqlalchemy import desc
from .common import try_except_log, response, delete_me
import logging, json, datetime
from app.exceptions import UserError
from tools.other_tools import random_str
from flask_paginate import Pagination, get_page_parameter

_logger = Flask(__name__).logger


# View 接口
@main.route('/user/tree', methods=['GET', 'POST'])
@login_required
def hs_user_tree():
    # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = HsUserSearch()
    ctx = {
        'ALLOW_DELETE': current_app.config.get('ALLOW_DELETE')
    }
    return render_template('hs_user_tree.html', name=session.get('name'), form=form, ctx=ctx)


@main.route('/user/form/', methods=['GET', 'POST'])
@main.route('/user/form/<int:record_id>', methods=['GET', 'POST'])
@login_required
def hs_user_form(record_id):
    this_obj = User
    form = HsUserForm()
    record = this_obj.query.filter_by(id=record_id).first()

    roles = Role.query.all()
    return render_template('hs_user_form.html', name=session.get('name'), form=form, record=record, roles=roles)


@main.route('/user/reset/password/form/', methods=['GET', 'POST'])
@main.route('/user/reset/password/form/<int:record_id>', methods=['GET', 'POST'])
@login_required
@try_except_log()
def user_reset_password_form(record_id):
    # 重置密码form
    ctx = {}
    form = HsUserResetPasswordForm()
    return render_template('hs_user_reset_password_form.html', name=session.get('name'), form=form, record_id=record_id)


# Api 创建或更新接口
@main.route('/user/create_update', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def user_create_update():
    this_obj = User

    data = request.form
    record_id = data.get('record_id', 0)

    print(data)

    if record_id:
        record = this_obj.query.filter_by(id=record_id).first()
    else:
        record = this_obj()
        record.password = random_str(6)

    username = data['username']
    email = data['email']

    if not username or not email:
        raise UserError("用户名和邮箱必填!")

    record.username = username
    record.email = email
    record.role_id = data['role_selection'] or None

    db.session.add(record)
    db.session.commit()

    return response({
        'record_id': record.id,
        'username': record.username,
        'email': record.email,
        'role_id': record.role_id,
    })


@main.route('/user/search', methods=['POST'])
@login_required
@try_except_log()
def find_hs_user():

    this_obj = User
    query = this_obj.query.order_by(desc(this_obj.id))

    form_data = request.form

    current_page = int(form_data.get('current_page') or 0)
    page_size = int(form_data.get('page_size') or 10)

    # 按照username搜索
    def find_username():
        if not request.form.get('content'):
            return query.paginate(current_page, page_size, error_out=False)
        return query.filter(this_obj.username.like('%'+request.form.get('content')+'%')).paginate(current_page, page_size, error_out=False)

    # 按照email搜索
    def find_email():
        if not request.form.get('content'):
            return query.paginate(current_page, page_size, error_out=False)
        return query.filter(this_obj.email.like('%' + request.form.get('content') + '%')).paginate(current_page, page_size, error_out=False)

    # 按照role搜索
    def find_role():
        if not request.form.get('content'):
            return query.paginate(current_page, page_size, error_out=False)
        roles = Role.query.filter(Role.name.like('%' + request.form.get('content') + '%')).all()
        role_ids = [role.id for role in roles] or [-1]
        return query.filter(this_obj.role_id.in_(role_ids)).paginate(current_page, page_size, error_out=False)

    methods = {
        'username': find_username,
        'email': find_email,
        'role': find_role,
    }

    paginate = methods[request.form.get('method')]()
    data = []

    for record in paginate.items:

        show_fields = [
            'id', 'name', 'email', 'username', 'role_name', 'create_date', 'update_time'
        ]

        item = {}
        for _field in show_fields:
            if _field == 'model_id':
                item[_field] = record.model_name
            else:
                item[_field] = getattr(record, _field)

        data.append(item)

    result = {
        'total': paginate.total,
        'data': data
    }

    return response(result)


@main.route('/user/delete', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def user_delete_new():
    # 哪一个模型, 要删除的对象名
    raise UserError("不允许删除用户")


@main.route('/user/reset/password', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True, null_body=True)
def user_reset_password():
    # 重置密码
    data = request.form
    password = data['password']
    user_id = data['user_id']
    user = User.query.filter_by(id=user_id).first()
    user.password = password
    user.generate_reset_token()
    db.session.add(user)
    db.session.commit()
    return response({})
