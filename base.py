# -*- coding: utf-8 -*-

from datetime import date
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
    https://www.codenong.com/43663552/
    使用Flask的jsonify时，将datetime.date保持为’yyyy-mm-dd’格式
    """
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat() #.replace('T', ' ')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
