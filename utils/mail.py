#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import zmail
from config import conf


def send_report(system_name, to_email, cc_email, result, report_file):
    '''
    发送报告
    :param system_name: 邮件报告名称
    :param to_email:  收件人
    :param result: 邮件内容
    :param report_file: 邮件附件
    :return:
    '''
    with open(conf.MAIL_REPORT_TEMPLATE, encoding='utf-8') as f:
        content_html = f.read()
    result['subject_info'] = system_name + conf.EMAIL_SUBJECT
    try:
        mail = {
            # 'subject': conf.EMAIL_SUBJECT,
            'subject': system_name + '测试环境接口自动化测试报告',
            'content_html': content_html.format(**result),
            'attachments': [report_file, ]
        }
        server = zmail.server(*conf.FROM_EMAIL_ADDRESSEE.values())
        # server.send_mail(conf.TO_EMAIL_ADDRESSEE, mail)
        server.send_mail(to_email, mail, cc=cc_email)
    except Exception as e:
        print("Error: 无法发送邮件，{}！", format(e))
    else:
        print("测试邮件发送成功！")


if __name__ == "__main__":
    '''请先在config/conf.py文件设置QQ邮箱的账号和密码'''
    pass
    # send_report()
