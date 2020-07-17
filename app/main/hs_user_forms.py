from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length


class HsUserSearch(FlaskForm):
    methods = [('username', 'User Name'), ('email', 'Email'), ('role', 'Role')]
    method = SelectField(choices=methods, validators=[DataRequired(message=u'名称不能为空')], coerce=str)
    content = StringField()
    submit = SubmitField('搜索')


class HsUserForm(FlaskForm):
    record_id = IntegerField(validators=[])

    username = StringField("User Name")
    email = StringField("Email")

    date = DateField("Date")
    submit = SubmitField('创建/更新')
    new_again = SubmitField('继续创建')


class HsUserResetPasswordForm(FlaskForm):
    record_id = IntegerField(validators=[])

    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')
