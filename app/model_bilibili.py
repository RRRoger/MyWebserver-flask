#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from . import db
from .models import User


class BilibiliBv(db.Model):
    __tablename__ = 'hs_bilibili_bv'

    id = db.Column(db.Integer, primary_key=True)
    bv_name = db.Column(db.String(255), index=True)

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


class BiliBvReply(db.Model):
    __tablename__ = 'hs_bilibili_bv_reply'

    id = db.Column(db.Integer, primary_key=True)
    bv_id = db.Column(db.Integer, db.ForeignKey('hs_bilibili_bv.id'))

    uname = db.Column(db.String(255), index=True)
    message = db.Column(db.Text)

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


class BiliLuckyDog(db.Model):
    __tablename__ = 'hs_bilibili_lucky_dog'

    id = db.Column(db.Integer, primary_key=True)
    bv_id = db.Column(db.Integer, db.ForeignKey('hs_bilibili_bv.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('hs_bilibili_bv_reply.id'))

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
