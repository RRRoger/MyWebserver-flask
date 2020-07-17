# -*- coding: utf-8 -*-
from flask import flash, request, url_for
from flask_login import current_user
from functools import wraps
from sqlalchemy import exc
from flask import jsonify
from app.exceptions import UserError
from app.model_api_log import HSApiLog
from flask import current_app
from app import db


def response(data):
    """
    返回接口使用的报文格式
    :param data:
    :return:
    """
    result = {
        'code': 0,
        'data': data,
    }
    return jsonify(result)


def try_except_log(add_log=False, null_body=False):
    """
    :param add_log: 是否创建日志
    :param null_body: 不记录报文数据
    :return:
    """
    def outer_wrapper(func):

        @wraps(func)
        def _wrapper(*args, **kw):

            # is_success: 接口成功/失败; current_user_id:当前用户id, result函数返回值
            is_success, result = True, jsonify({})

            try:
                result = func(*args, **kw)
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                is_success = False
                result = jsonify({'code': -10001, 'msg': "唯一性验证报错, 请不要重复创建!"})
            except exc.OperationalError as e:
                db.session.rollback()
                is_success = False
                result = jsonify({'code': -10002, 'msg': "数据库操作错误: %s" % str(e)})
            except UserError as e:
                db.session.rollback()
                is_success = False
                result = jsonify({'code': -10003, 'msg': "错误: %s" % str(e)})
            except Exception as e:
                db.session.rollback()
                is_success = False
                result = jsonify({'code': -10000, 'msg': "系统错误: %s" % str(e)})
            finally:
                current_user_id = None if current_user.is_anonymous else current_user.id
                # 添加用户操作日志, 只有用户id存在才创建
                if add_log and current_user_id:

                    response_body = ''
                    if hasattr(result, 'data'):
                        response_body = result.data

                    # 特殊场景不记录报文
                    form_body = str(request.form)
                    file_body = str(request.files)
                    data_body = str(request.data)

                    if null_body:
                        form_body = '[has been cleared]'
                        file_body = '[has been cleared]'
                        data_body = '[has been cleared]'
                        response_body = '[has been cleared]'

                    log = HSApiLog(
                        is_success=is_success, url=request.path, remote_addr=request.remote_addr,
                        form_body=form_body, file_body=file_body, data_body=data_body,
                        response_body=response_body, create_uid=current_user_id,
                    )
                    db.session.add(log)
                    db.session.commit()
                return result

        return _wrapper

    return outer_wrapper


def delete_me(db, clazz, context=None):
    """
    删除model, 通用函数
    :param db: database
    :param clazz: 对象clazz
    :param context: 上下文
    :return:
    """

    allow_delete = current_app.config.get('ALLOW_DELETE')
    if not allow_delete:
        raise UserError("不允许删除任何记录!")

    data = request.form
    record_id = data['record_id']
    records = clazz.query.filter_by(id=record_id).first_or_404()
    db.session.delete(records)
    db.session.commit()
    return True
