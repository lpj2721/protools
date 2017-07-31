# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/31 17:11
"""

import pytest

from framework.flask.intercept.before_request import parse_path


@pytest.mark.parametrize("path, prefix, api, excepted", [
    ("/api/cloud/v1/template/add", "/api/cloud", True, ("v1", "/template/add")),
    ("/api/cloud/v1/template/add", "api/cloud/", True, ("v1", "/template/add")),
    ("/v1/template/add", "", True, ("v1", "/template/add")),
    ("/api/cloud/template/add", "/api/cloud", False, ("", "/template/add")),
    ("/template/add", "", False, ("", "/template/add")),
    ("/v1/template/add", "xxxxx", True, ("", "")),
    ("/v1/template/add", "/template/add", True, ("", ""))
])
def test_parse_path(path, prefix, api, excepted):
    assert parse_path(path, prefix, api) == excepted


if __name__ == '__main__':
    args = ["-vv", "--color", "yes", "test_before_request.py"]
    pytest.main(args)
