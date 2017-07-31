#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 16:29
"""
import re


def is_mobile(instance):
    _mobile_re = re.compile(r"^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])[0-9]{8}$")
    if not _mobile_re.match(instance):
        return False

# if __name__ == '__main__':
#      a = "13247780947"
#      b = is_mobile(a)
#      print b