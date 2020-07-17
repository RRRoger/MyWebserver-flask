# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, url_for
from . import main
from ..models import User, Post
from flask import render_template, session
from flask_login import login_user, logout_user, login_required
from .hs_api_log_forms import HsApiLogSearch, HsApiLogForm
from ..model_api_log import HSApiLog
from flask import Flask
from .. import db
from sqlalchemy import desc
from .common import try_except_log, response, delete_me
import logging
from app.exceptions import UserError
_logger = Flask(__name__).logger
from flask_paginate import Pagination, get_page_parameter


# View 接口
@main.route('/api_log/tree', methods=['GET', 'POST'])
@login_required
def hs_api_log_tree():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = HsApiLogSearch()
    ctx = {
        'ALLOW_DELETE': current_app.config.get('ALLOW_DELETE')
    }
    return render_template('hs_api_log_tree.html', name=session.get('name'), form=form, ctx=ctx)


@main.route('/api_log/form/', methods=['GET', 'POST'])
@main.route('/api_log/form/<int:record_id>', methods=['GET', 'POST'])
@login_required
def hs_api_log_form(record_id):
    this_obj = HSApiLog

    form = HsApiLogForm()
    record = this_obj.query.filter_by(id=record_id).first()
    return render_template('hs_api_log_form.html', name=session.get('name'), form=form, record=record)


# Api 接口
@main.route('/api_log-create-update', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def api_log_create_update():
    this_obj = HSApiLog

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
        'url': record.url,
        'create_date': record.create_date,
        'update_time': record.update_time,
        'create_uid': record.create_uid,
        'is_success': record.is_success,
    })


@main.route('/api_log/search', methods=['POST'])
@login_required
@try_except_log()
def find_hs_api_log():

    this_obj = HSApiLog
    query = this_obj.query.order_by(desc(this_obj.id))

    form_data = request.form

    current_page = int(form_data.get('current_page') or 0)
    page_size = int(form_data.get('page_size') or 10)

    # 按照某个字段搜索
    def find_url():
        if not form_data.get('content'):
            return query.order_by('id').paginate(current_page, page_size, error_out=False)
        return query.order_by('id').filter(this_obj.url.like('%'+form_data.get('content')+'%')).paginate(current_page, page_size, error_out=False)

    def find_remote_addr():
        if not form_data.get('content'):
            return query.order_by('id').paginate(current_page, page_size, error_out=False)
        return query.order_by('id').filter(this_obj.remote_addr.like('%'+form_data.get('content')+'%')).paginate(current_page, page_size, error_out=False)

    # 按照create_uid字段搜索
    def find_create_uid():
        if not form_data.get('content'):
            return query.paginate(current_page, page_size, error_out=False)
        insts = User.query.filter(User.username.like('%' + request.form.get('content') + '%')).all()
        inst_ids = [inst.id for inst in insts] or [-1]
        return query.filter(this_obj.create_uid.in_(inst_ids)).paginate(current_page, page_size, error_out=False)

    # 按照create_uid字段搜索
    def find_is_success():
        if not form_data.get('content'):
            return query.paginate(current_page, page_size, error_out=False)

        return query.filter(this_obj.is_success.is_(form_data['content'] == '1')).paginate(current_page, page_size, error_out=False)

    methods = {
        'url': find_url,  # 对应上面的某一个函数
        'create_uid': find_create_uid,  # 对应上面的某一个函数
        'is_success': find_is_success,  # 对应上面的某一个函数
        'remote_addr': find_remote_addr,  # 对应上面的某一个函数
    }

    paginate = methods[form_data.get('method')]()
    data = []
    for record in paginate.items:
        item = {
            'id': record.id,
            'url': record.url,
            'remote_addr': record.remote_addr,
            'is_success': record.is_success,
            'create_date': record.create_date,
            'update_time': record.update_time,
            'create_user_name': record.create_user_name,
        }
        data.append(item)

    result = {
        'total': paginate.total,
        'data': data
    }

    return response(result)


@main.route('/api_log-delete', methods=['GET', 'POST'])
@login_required
@try_except_log(add_log=True)
def api_log_delete_new():
    # 哪一个模型, 要删除的对象名
    raise UserError("不允许删除用户")

