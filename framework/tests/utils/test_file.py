# encoding: utf-8

"""
@version: 1.0
@author: emrick
@contact: yeemrick@gmail.com
@time: 2017/3/24 14:17
"""

import pytest

from framework.utils.file import get_ini_dict, get_file_path


def test_get_ini_dict():
    file_path = get_file_path("tests", "conf", "test.conf")
    conf_dict = get_ini_dict(file_path)
    test_dict = {
        'section0': {
            'key0': 'val0',
            'key1': 'val1',
            'key2': ''
        },
        'section1': {

        }
    }
    assert conf_dict.__cmp__(test_dict) == 0

if __name__ == '__main__':
    pytest.main()