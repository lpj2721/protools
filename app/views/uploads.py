#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/21 12:51
"""
import os
from flask import request, url_for, send_from_directory
from app.conf.config import web
from werkzeug.utils import secure_filename
from framework.flask import app
from framework.decorators import route
from framework.utils.common import get_ret,build_ret
from framework.db import db
from app.models.company_info import company_info
collection = db['mongodb']

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


app.config['UPLOAD_FOLDER'] = web['upload_path']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        username = request.user_name
        file_key = request.files.keys()[0]
        file = request.files[file_key]
        if file and allowed_file(file.filename):
            filename = file.filename
            files_path = check_file_path(app.config['UPLOAD_FOLDER'], username)
            file.save(os.path.join(files_path , filename))
            file_url = web['pic_pix'] + "uploads/" + username + "/" + filename
            company = company_info(username)
            if file_key == "logo":
                company['logo'] = file_url
            elif file_key == "license":
                company['production_license'] = file_url
            elif file_key == "organization":
                company['organization_code'] = file_url
                collection['CompanyInfo'].update_one(company, {"$set": company})
            result = {
                'file_url': file_url
            }
            return build_ret(success=True, data=result)
    return html


def check_file_path(file_path,username):
    file_dir = os.path.join(file_path, username)
    # 判断存储路径是否存在
    if os.path.isdir(file_dir):
        return file_dir
    else:
        os.chdir(file_path)
        os.mkdir(username)
        return file_dir



