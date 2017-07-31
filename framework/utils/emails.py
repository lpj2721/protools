# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2017/3/28 14:02
"""
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.conf.config import email
from framework.utils import logging


def sendmail(toaddrs, subject=email["subject"], msg=None):
    """
    :param toaddrs: 收件人地址可多个["",""]
    :param subject: 邮件主题
    :param msg: 邮件内容
    :return:
    """
    mail_msg = MIMEMultipart()
    if not isinstance(subject, unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] = email["from_email"]
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL()
        s.connect(email["smtp_addr"])
        s.login(email["from_email"], email["from_email_pwd"])
        s.sendmail(email["from_email"], toaddrs, mail_msg.as_string())
        s.quit()
        logging.info("email send sucess. %s", ','.join(toaddrs))
    except IOError:
        logging.error("Error unable to send email. %s", traceback.format_exc())
