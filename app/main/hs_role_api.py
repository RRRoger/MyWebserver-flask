# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, url_for
from . import main
from ..models import User, Post
from flask import render_template, session
from flask_login import login_user, logout_user, login_required
from .hs_role_forms import HsRoleSearch, HsRoleForm
from ..models import Role
from flask import Flask
from .. import db
from sqlalchemy import desc
from .common import try_except_log, response, delete_me
import logging
from flask_paginate import Pagination, get_page_parameter
from app.exceptions import UserError
_logger = Flask(__name__).logger


# View 接口
@main.route('/role/tree', methods=['GET', 'POST'])
@login_required
def hs_role_tree():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = HsRoleSearch()
    ctx = {
        'ALLOW_DELETE': current_app.config.get('ALLOW_DELETE')
    }
    return render_template('hs_role_tree.html', name=session.get('name'), form=form, ctx=ctx)


@main.route('/role/form/', methods=['GET', 'POST'])
@main.route('/role/form/<int:record_id>', methods=['GET', 'POST'])
@login_required
def hs_role_form(record_id):
    this_obj = Role

    form = HsRoleForm()
    record = this_obj.query.filter_by(id=record_id).first()
    return render_template('hs_role_form.html', name=session.get('name'), form=form, record=record)


# Api 接口
@main.route('/role-create-update', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def role_create_update():
    this_obj = Role

    # 哪一个模型, 要删除的对象名
    data = request.form
    _logger.info(data)
    record_id = data['record_id']

    if record_id:
        record = this_obj.query.filter_by(id=record_id).first()
    else:
        record = this_obj()

    record.name = data['name']

    db.session.add(record)
    db.session.commit()
    return response({
        'record_id': record.id,
        'name': record.name
    })


@main.route('/role/search', methods=['POST'])
@login_required
@try_except_log()
def find_hs_role():

    this_obj = Role
    query = this_obj.query.order_by(desc(this_obj.id))

    form_data = request.form

    current_page = int(form_data.get('current_page') or 0)
    page_size = int(form_data.get('page_size') or 10)

    # 按照某个字段搜索
    def find_name():
        if not form_data.get('content'):
            return query.paginate(current_page, page_size, error_out=False)
        return query.filter(this_obj.name.like('%'+form_data.get('content')+'%')).paginate(current_page, page_size, error_out=False)

    methods = {
        'name': find_name,  # 对应上面的某一个函数
    }

    paginate = methods[request.form.get('method')]()
    data = []
    for record in paginate.items:
        item = {
            'id': record.id,
            'name': record.name,
            'create_date': record.create_date,
            'update_time': record.update_time,
        }
        data.append(item)

    result = {
        'total': paginate.total,
        'data': data
    }

    return response(result)


@main.route('/role-delete', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def role_delete_new():
    # 哪一个模型, 要删除的对象名
    raise UserError("不允许删除用户")

