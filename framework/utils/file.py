# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2016/11/14 10:08
"""
import os
from ConfigParser import ConfigParser
from os import path


def get_file_path(*args):
    """
    根据args从根目录获取文件的绝对路径
    :param args: 例如 get_file_path("1","2","3.xml") -> ${root_dir}/1/2/3.xml
    :return: 文件的绝对路径
    """
    previous_path = "/../../../"
    root_dir = path.abspath(__file__ + previous_path)
    for arg in args:
        if isinstance(arg, tuple):
            for a in arg:
                root_dir = path.join(root_dir, a)
        else:
            root_dir = path.join(root_dir, arg)
    return root_dir


def get_ini_dict(filepath):
    """
    获取ini文件中内容字典
    :param filepath:
    :return:
    """
    with open(filepath) as conffile:
        ini_config = ConfigParser()
        ini_config.readfp(conffile)
        result_dict = {}
        for section in ini_config.sections():
            result_dict[section] = {}
            for key in ini_config.options(section):
                result_dict[section][key] = ini_config.get(section, key)
        return result_dict


def package_import(package, excludes=None):
    """
    引用包内的所有py文件
    :param excludes: type(list) 需要排除文件名称
    :param package: type(str)包路径, 多级路径用 . 分隔, 例如 user.config.pkg
    :return:
    """
    if excludes is None:
        excludes = []
    try:
        dir_path = package.replace(".", os.sep)
        files = get_dir_files_with_py(dir_path)
        files = [x for x in files if x not in excludes]
        packages = [package + "." + x for x in files]
        for pkg in packages:
            __import__(pkg)
    except OSError:
        raise ValueError("package [%s] not exists, please checking!" % package)


def get_dir_files_with_py(dir_path):
    """
    获取当前路径下所有py文件
    :param dir_path: 相对项目根目录的路径
    :return:
    """
    abs_path = get_file_path(dir_path)
    files = [x.replace(".py", "") for x in os.listdir(abs_path) if "__" not in x and "pyc" not in x]
    return files
