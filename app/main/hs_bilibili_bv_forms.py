# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length


class HsBilibiliBvSearch(FlaskForm):
    methods = [('bv_name', 'bv_name')]
    method = SelectField(choices=methods, validators=[DataRequired(message=u'名称不能为空')], coerce=str)
    content = StringField()
    submit = SubmitField('搜索')


class HsBilibiliBvForm(FlaskForm):
    record_id = IntegerField(validators=[])
    bv_name = StringField(validators=[DataRequired(message=u'名称不能为空')])
    submit = SubmitField('创建')
    new_again = SubmitField('继续创建')
