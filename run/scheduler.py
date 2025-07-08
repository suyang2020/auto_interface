#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: suyang
# @Last Modified by:   suyang
# @Date:   2025-3-4 10:00:00
import os

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from utils import logger
from config import conf
from run.jmeter_api import JmeterApi
from run.jtl_api import JtlApi
from utils import mail, times
from testcases import live_test
from utils.tools import message_to_wechat
from testcases import obs
import threading


# def run_testcase(project_name, system_name,type=""):
#     if type=="创建直播":
#         live_test.test_add_live()


def run_script(project_name, system_name, script_name, to_email, cc_email):
    '''
    执行脚本并发送邮件
    :param system_name: 系统名称，如：直播
    :param script_name: 脚本名称，如：auto_test_live
    :param to_email:  收件人
    :param cc_email:  抄送人
    :return:
    '''
    jtl = JtlApi()
    log_file = conf.LOG_DIR + '/jmeter-' + times.datetime_strftime('%Y%m%d') + '.log'  # 生成的日志路径
    script_jmx_file = conf.SCRIPT_DIR + '/' + system_name+ '/' + script_name + '.jmx'  # 执行的jmx脚本文件
    result_jtl_file = conf.RESULT_DIR + '/' + script_name + '.jtl'  # 生成的ljt结果文件
    report_file = conf.REPORT_DIR + '/' + script_name + '_report.html'  # 生成的html报告文件

    JmeterApi().script_jmx(conf.JMETER_PATH, result_jtl_file, script_jmx_file, log_file)
    result_list = jtl.jtlToJson(result_jtl_file)

    jtl.reportDetail(report_file, result_list)
    email_result_dict = jtl.emailSummaryStatistics(result_list)

    if email_result_dict.get('failed') != '0':
        # pass
        # mail.send_report(system_name, to_email, cc_email, email_result_dict, report_file)
        message_to_wechat(result_list, "直播接口", "直播")


    return email_result_dict


def creat_index_html(project_name_dict):
    '''
    创建index文件
    :param project_name_dict: 项目名称：{系统名称: 脚本名称}
    :return:
    '''
    jtl = JtlApi()
    index_report_file = conf.REPORT_DIR + '/index.html'
    jtl.indexReport(project_name_dict, index_report_file)


def scheduler(system_name, project_name):
    '''
    调度
    :param system_name: 系统名字
    :param project_name: 项目名
    :return:
    '''
    project_name_dict = {}
    system_name_dict = {}

    if project_name in conf.PROJECT_NAME_DICT.keys():
        if system_name in conf.PROJECT_NAME_DICT.get(project_name).keys():
            script_name = conf.PROJECT_NAME_DICT.get(project_name).get(system_name)
            to_email = conf.TO_EMAIL_DICT.get(project_name).get(system_name)
            cc_email = conf.CC_EMAIL_ADDRESSEE.get(project_name)

            result_dict = run_script(project_name, system_name, script_name, to_email, cc_email)
            system_name_dict[system_name] = script_name
            project_name_dict[project_name] = system_name_dict
        else:
            for system_name, script_name in conf.PROJECT_NAME_DICT.get(project_name).items():
                to_email = conf.TO_EMAIL_DICT.get(project_name).get(system_name)
                cc_email = conf.CC_EMAIL_ADDRESSEE.get(project_name)
                run_script(project_name, system_name, script_name, to_email, cc_email)
                system_name_dict[system_name] = script_name
            project_name_dict[project_name] = system_name_dict
        creat_index_html(project_name_dict)
    else:
        return
    return result_dict




# login
def get_authorization():
    """
    获取后台管理的token
    :return:
    """
    # host = conf.HOST
    # url = host + "/login"
    #
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "accountNo": "shop152",
    #     "password": "shop152",
    #     "validCode": "",
    #     "validCodeReqNo": "",
    #     "userType": "",
    #     "loginType": "",
    #     "device": "PC"
    # }
    #
    # response = requests.post(url, headers=headers, data=json.dumps(data))
    #
    # if response.status_code == 200:
    #     data = response.json()
    #
    #     authorization = "Bearer " + data["data"]["token"]
    #     return authorization
    # else:
    #     return "get token error"
    authorization = "Bearer meVwGVjYE7Aj2jhb7yDT2iMxe7tgyKpWhJZ7VpdinGuy5bHtRvXeOMHaiAm7ZtHVJDyE4AhzBvohnFVoahI8YKYkwbayufgXIKo42GrYBYuNjZiKDycTeT0RlXB2fXof"
    return authorization

def stream(push_url, pull_url):

    # 检查有没有mp4文件，

    # 启动推流线程
    push_thread = threading.Thread(target=obs.push_obs, args=(push_url, 200))
    push_thread.start()

    # 等待推流启动
    time.sleep(10)

    # 启动拉流线程
    pull_thread = threading.Thread(target=obs.pull_obs, args=(pull_url, 20))
    pull_thread.start()

    # 等待拉流完成
    pull_thread.join()
    # scheduler(system_name, project_name)

    # 检查拉取的视频文件是否正常
    # if check_video_file(output_file):
    #     print("直播拉流测试通过！")
    # else:
    #     print("直播拉流测试失败！")

    # 等待推流线程结束
    push_thread.join()


def run_testcases():

    authorization = get_authorization()
    tl = live_test.TestLive(authorization)
    # 创建直播
    live_id = tl.test_add_live()
    if live_id:
        # 开启直播
        tl.test_start_live(live_id)
    # 创建循环伪直播
    live_record_id = tl.test_add_record_live()

    # 给直播增加签名
    if live_id:
        tl.test_live_sign(live_id)
    if live_id:
        # 分享直播，获取分享地址和推流地址
        share_rul, push_url, pull_url = tl.test_share_live(live_id)
    # 分享伪直播，获取分享地址
    # share_record_url = tl.test_share_live(live_record_id)[0]
    # 关闭循环伪直播
    if live_record_id:
        tl.test_end_live(live_record_id)

    # 创建伪直播
    live_pre_record_id = tl.test_add_pre_record_live()

    # 分享录播，获取分享地址
    # share_cycle_record_url = tl.test_share_live(live_cycle_record_id)[0]
    # 直播推流
    # obs.push_obs(push_url, 420)

    if live_id:
        # 签名列表检查
        tl.test_sign_list(live_id)
    # 关闭伪直播
    if live_pre_record_id:
        tl.test_end_live(live_pre_record_id)

    # 测试推流和拉流
    if live_id:
        stream(push_url, pull_url)

    # 另外一个线程去执行前端h5接口
    scheduler(system_name, project_name)

    # 关闭直播
    if live_id:
        tl.test_end_live(live_id)


if __name__ == '__main__':
    # args_list = sys.argv
    # system_name = args_list[1]
    # project_name = args_list[2]

    system_name = '直播'
    # system_name = '性能'
    project_name = '微鲸灵'

    # if system_name == "直播h5接口":
    #     run_testcases()
    scheduler(system_name, project_name)





