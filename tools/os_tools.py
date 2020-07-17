# -*- coding: utf-8 -*-
import os


def os_mkdir(dir_path, name):
    """
    创建目录, 如果存在则不创建
    最终返回目录的绝对路径
    :param dir_path:
    :param name:
    :return: your dir path
    """
    path = os.path.join(dir_path, name)
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        return path
    else:
        return path


def os_remove(path):
    """
    删除文件目录
    :param path:
    :return:
    """
    os.remove(path)
    return True


def os_save_temp_file(current_app, file_name, data, parent_dir=None):
    """
    创建临时文件
    :param current_app: 当前app
    :param file_name: 文件名
    :param data: 文件流数据
    :param parent_dir: 上级目录
    :return:
    """
    dir_path = current_app.config['TEMP_DIR_PATH']

    # 如果传上级目录, 则文件保存在此目录下
    if parent_dir:
        dir_path = os_mkdir(dir_path, parent_dir)

    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'wb') as f:
        f.write(data)

    return file_path


if __name__ == "__main__":
    HOME_PATH = os.path.expanduser('~')
    print(os_mkdir(HOME_PATH, 'test'))

