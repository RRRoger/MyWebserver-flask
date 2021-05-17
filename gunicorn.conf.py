# -*- coding: utf-8 -*-
import os
import multiprocessing

# FIX import requets error:
# see https://github.com/gevent/gevent/issues/1016
import gevent.monkey
gevent.monkey.patch_all()
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
create_urllib3_context()

workers = multiprocessing.cpu_count() * 2 + 1    #进程数
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:5000"
# timeout = 30      #超时

loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s"'    # 设置gunicorn访问日志格式，错误日志无法设置

home_path = os.path.expanduser('~')
accesslog = os.path.join(home_path, 'log', "gunicorn_access.log")  # http 访问日志
errorlog = os.path.join(home_path, 'log', "gunicorn_info.log")  # 系统日志, 包含主动打印的INFO




"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
