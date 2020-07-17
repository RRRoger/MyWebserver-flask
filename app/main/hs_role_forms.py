from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length


class HsRoleSearch(FlaskForm):
    methods = [('name', 'Name')]
    method = SelectField(choices=methods, validators=[DataRequired(message=u'名称不能为空')], coerce=str)
    content = StringField()
    submit = SubmitField('搜索')


class HsRoleForm(FlaskForm):
    record_id = IntegerField(validators=[])
    name = StringField(validators=[DataRequired(message=u'名称不能为空')])
    submit = SubmitField('创建/更新')
    new_again = SubmitField('继续创建')
