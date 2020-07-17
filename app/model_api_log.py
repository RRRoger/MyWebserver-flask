from datetime import datetime
from . import db
from .models import User


class HSApiLog(db.Model):
    __tablename__ = 'hs_api_log'
    _description = "接口日志"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), index=True)
    remote_addr = db.Column(db.String(255), index=True)

    is_success = db.Column(db.Boolean, default=True)

    form_body = db.Column(db.Text)
    data_body = db.Column(db.Text)
    file_body = db.Column(db.Text)

    response_body = db.Column(db.Text)

    create_date = db.Column(db.DateTime, default=datetime.now, index=True)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    create_uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def create_user_name(self):
        """
        获取外键model_id对应的name
        :return:
        """
        if self.create_uid:
            record = User.query.filter_by(id=self.create_uid).first()
            return record.username
        else:
            return ''
