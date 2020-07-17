Flasky
======

This repository contains the source code examples for the second edition of my O'Reilly book [Flask Web Development](http://www.flaskbook.com).

The commits and tags in this repository were carefully created to match the sequence in which concepts are presented in the book. Please read the section titled "How to Work with the Example Code" in the book's preface for instructions.

For Readers of the First Edition of the Book
--------------------------------------------

The code examples for the first edition of the book were moved to a different repository: [https://github.com/miguelgrinberg/flasky-first-edition](https://github.com/miguelgrinberg/flasky-first-edition).



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

flask init-tables
```

## Show Dir Tree

```bash
tree -I 'node_modules|cache|layui|__pycache__|ca' -d > ./dir_tree.txt
```