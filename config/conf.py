#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import subprocess

#测试环境
#host地址
HOST = 'http://111.172.196.67:11002'
# # #素材ID
MATERIAL_ID = "473500939995750401"

# 生产环境
# HOST = 'http://14.22.85.178:11002'
# MATERIAL_ID = "497091654726066176"



# 项目目录
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 脚本执行日志目录
LOG_DIR = os.path.join(BASE_DIR, 'log')

# 报告目录
REPORT_DIR = os.path.join(BASE_DIR, 'report')

# 报告样式
MAIL_REPORT_TEMPLATE = os.path.join(BASE_DIR, 'template', 'mail_report_template.html')

REPORT_DETAIL_TEMPLATE = os.path.join(BASE_DIR, 'template', 'report_detail_template.html')

RESULT_DETAIL_TEMPLATE = os.path.join(BASE_DIR, 'template', 'result_detail_template.html')

RESULT_SUMMARY_TEMPLATE = os.path.join(BASE_DIR, 'template', 'result_summary_template.html')

INDEX_REPORT_TEMPLATE = os.path.join(BASE_DIR, 'template', 'index.html')

# 接口脚本目录
SCRIPT_DIR = os.path.join(BASE_DIR, 'script')

# 接口结果目录
RESULT_DIR = os.path.join(BASE_DIR, 'result')

# Jmeter执行目录
# JMETER_PATH = r'''".\apache-jmeter-5.3\bin\jmeter.bat"'''
# JMETER_PATH=r'''"D:\software\apache-jmeter-5.3/bin/jmeter"'''
import os

# 获取当前项目的根目录
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 构建 jmeter.sh 的完整路径
JMETER_PATH = os.path.join(project_root, 'apache-jmeter-5.6.3', 'bin', 'jmeter')

os.path.join(project_root, 'apache-jmeter-5.6.3', 'bin', 'jmeter')

# if os.name == 'nt':  # Windows
#     JMETER_PATH = os.path.join(project_root, 'apache-jmeter-5.3', 'bin', 'jmeter')
# else:  # Linux
#     JMETER_PATH = os.path.join(project_root, 'apache-jmeter-5.3', 'bin', 'jmeter')




# 项目信息
PROJECT_NAME_DICT =  {'微鲸灵': {
                              '直播': 'auto_test_live_auto',
                                '性能': 'auto_test_live'
                              },
                    '后台管理': {
                        '模块1': 'auto_test_user_center',
                        '模块2': 'auto_test_live'
                                },
                    '商城': {
                          '模块2': 'auto_test_user_center',
                          '模块1': 'auto_test_live'
                             }
                      }


# 项目文件夹
PROJECT_FOLDER = ['直播','后台管理','商城']

# 发件人地址
FROM_EMAIL_ADDRESSEE = {
    'username': 'public_tech@medbanks.cn',  # 切换成你自己的地址
    'password': 'Sipai321456',
    'smtp_host': 'smtp.exmail.qq.com',
    'smtp_port': 465
}

# 收件人地址
TO_EMAIL_DICT = {'微鲸灵': {
                          '模块2': ['yang.su@medbanks.cn'],
                          '直播h5接口': ['suyang_hebei@163.com']
                          },
                '后台管理': {
                          '模块2': ['yang.su@medbanks.cn'],
                          '模块1': ['suyang_hebei@163.com']
                          },
                '商城': {
                          '模块1': ['yang.su@medbanks.cn'],
                          '模块2': ['suyang_hebei@163.com']
                          }
                 }

# 抄送人地址
CC_EMAIL_ADDRESSEE = {'直播':  ['suyang_hebei@163.com'],
                '后台管理': ['suyang_hebei@163.com'],
                '商城': ['suyang_hebei@163.com']
                 }

# 邮件主题
EMAIL_SUBJECT = '测试环境接口自动化测试报告'

# 企业微信报警机器人
# EMERGENCY_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=84373787-11cc-486c-a21c-a01cbcb7f81c"
EMERGENCY_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=66247371-af06-4b90-9a98-d51f08b1de14"

if __name__ == "__main__":
    print(BASE_DIR)
    # print(REPORT_PATH)
