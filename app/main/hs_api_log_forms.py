from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length


class HsApiLogSearch(FlaskForm):
    methods = [
        ('url', 'URL'),
        ('create_uid', 'Create User'),
        ('is_success', 'Is Success'),
        ('remote_addr', 'Remote Address'),
    ]
    method = SelectField(choices=methods, validators=[DataRequired(message=u'名称不能为空')], coerce=str)
    content = StringField()
    submit = SubmitField('搜索')


class HsApiLogForm(FlaskForm):
    record_id = IntegerField(validators=[])
    url = StringField()
    remote_addr = StringField()

    is_success = BooleanField()

    form_body = TextAreaField()
    data_body = TextAreaField()
    file_body = TextAreaField()
    response_body = TextAreaField()

    create_date = StringField()
    create_user_name = StringField()
