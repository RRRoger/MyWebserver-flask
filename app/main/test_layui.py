# -*- coding: utf-8 -*-

from . import main
from flask import render_template, session
from flask_login import login_user, logout_user, login_required
from .hs_model_forms import HsModelSearch, HsModelForm
from flask import Flask

_logger = Flask(__name__).logger


# View 接口
@main.route('/test_lay_ui', methods=['GET', 'POST'])
@login_required
def test_lay_ui():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    return render_template('test_layui.html', name=session.get('name'))
