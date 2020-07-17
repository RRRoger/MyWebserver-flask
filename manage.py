# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate
from hello import app


manager = Manager(app)


# 定义自己要执行的command
@manager.command
def test():
    print(u'test run')


if __name__ == '__main__':
    manager.run()
