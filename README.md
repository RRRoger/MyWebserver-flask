# My WebServer

> 网站模板
> 基于 Python3 + Flask + Mysql + Layui
>
> 包含用户管理, 角色管理, 接口日志 等基础内容
>
> 支持基本的增删改查操作, 搜索, 分页, 异常捕获与权限管理等


# Technology stack

- Python3.*
- Flask
- Mysql
- Layui

## Init

- 1. 添加环境变量

```bash
export FLASK_APP=hello.py
```

- 2. 创建数据库

```bash
create database test_db charset=utf8;
```

- 3. 初始化数据库

```bash
flask db init

flask db migrate

flask db upgrade

# 初始化用户数据
flask init-tables
```

