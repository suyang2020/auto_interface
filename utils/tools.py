import json
import os
import yaml
from utils import logger
from config import conf
from utils import times
import requests


def convert_json_to_dict(swagger_json):
    """ convert HAR data list to mapping

    Args:
        swagger_json (list)
            {"name": "v", "value": "1"},


    Returns:
        dict:
            {"v": "1", "w": "2"}

    """
    return json.loads(swagger_json)


def ensure_path_sep(path):
    """ ensure compatibility with different path separators of Linux and Windows
    确保与Linux和Windows的不同路径分隔符兼容
    os.sep.join会根据操作系统不同，将路径中间的符号搞成不同的符号
    等同于os.path.join(),但是两个方法传参不同，第一个方法传参为列表["E","demo"],第二个传参为os.path.join("E","demo","sy")
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return path


def dump_yaml(testcase, yaml_file):
    """ dump HAR entries to yaml testcase
    """
    logger.log.info("dump testcase to YAML format.")

    with open(yaml_file, "w", encoding="utf-8") as outfile:
        yaml.dump(
            testcase, outfile, allow_unicode=True, default_flow_style=False, indent=4
        )

    logger.log.info("Generate YAML testcase successfully: {}".format(yaml_file))



# 自己接企业微信的群报警机器人
def message_to_wechat(result_list, project_name, system_name):

    rep = ""
    for content in result_list:
        if content["result"] == "false":
            # print(content)

            # 机器人地址
            try:
                url = conf.EMERGENCY_URL
            except Exception:
                return
            header = {"Content-Type": "application/json"}

            # 拼发送内容
            request = content["java.net.URL"]
            try:
                responseDatas = json.loads(content["responseData"])
            except Exception as e:
                responseDatas = " "
            queryString = content["queryString"]
            date_time = times.current_time()
            mentioned_list = conf.EMERGENCY_URL

            try:
                responseData = responseDatas["message"]
            except Exception:
                responseData = "缺少异常提示"

            form_data = {
                "msgtype": "text",
                "text": {
                    "content": "{0}-测试环境\n请求地址:{1}\n请求参数:{2}\n异常信息:{3}\n报警时间:{4}".format(
                        system_name, request, queryString, responseData, date_time
                    ),
                    "mentioned_list": ["苏杨"],
                },
            }

            # 创建session对象，发起机器人发消息的请求
            # s = requests.session()

            try:
                rep = requests.post(
                    url=url, data=json.dumps(form_data).encode("utf-8"), headers=header
                )
            except Exception as e:
                logger.log.error("发送企业微信消息失败")
                return

            if rep.status_code != 200:
                print("request failed.")
                return

    return json.loads(rep.content)


# 自己接企业微信的群报警机器人
def message_to_wechat2(result_list):

    # 根据项目名获得机器人地址
    try:
        url = conf.EMERGENCY_URL
    except Exception:
        return
    header = {"Content-Type": "application/json"}

    # 拼发送内容

    date_time = times.current_time()
    mentioned_list = conf.EMERGENCY_URL
    request = result_list["url"]
    queryString = result_list["form_data"]

    try:
        responseData = result_list["rep"]["message"]
    except Exception:
         responseData = "缺少异常提示"

    form_data = {
        "msgtype": "text",
        "text": {
            "content": "{0}-测试环境\n请求地址:{1}\n请求参数:{2}\n异常信息:{3}\n报警时间:{4}".format(
                 "直播后台管理", request, queryString, responseData, date_time
            )
        },
    }

    # 创建session对象，发起机器人发消息的请求
    # s = requests.session()

    try:
        rep = requests.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=header, verify=False
        )
    except Exception as e:
        logger.log.error("发送企业微信消息失败")
        return

    if rep.status_code != 200:
        print("request failed.")
        return

    return json.loads(rep.content)


import pytest
# import requests
import datetime

# 企业微信机器人Webhook地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_webhook_key"


# def send_wechat_alert(test_name, request_url, request_params, error_message):
#     alert_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     message = {
#         "msgtype": "text",
#         "text": {
#             "content": f"直播-测试环境\n请求地址: {request_url}\n请求参数: {request_params}\n异常信息: {error_message}\n报警时间: {alert_time}"
#         }
#     }
#     response = requests.post(WEBHOOK_URL, json=message)
#     if response.status_code != 200:
#         print("Failed to send WeChat alert")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 获取测试用例名称
        test_name = item.name

        # 从测试用例的 request 对象中获取请求地址和请求参数
        request_url = getattr(item.function, "request_url", None)
        request_params = getattr(item.function, "request_params", None)

        # 获取异常信息
        error_message = str(rep.longrepr)

        result = {"url": request_url, "form_data": request_params, "rep": error_message}
        # message_to_wechat2(result)

        # 发送企业微信报警
        if request_url and request_params:
            message_to_wechat2(result)


# 示例测试用例
def test_example(request):
    # 设置请求地址和请求参数
    request_url = "http://111.172.196.67:11003/api/v2/live/enter"
    request_params = '{"liveId":""}'

    # 将请求地址和请求参数附加到测试函数上
    test_example.request_url = request_url
    test_example.request_params = request_params

    # 模拟测试失败
    assert 1 == 2, "未找到直播间"















if __name__ == '__main__':
    a = {"key1": "value1", "key2": [1, 2, "str test", 5]}
    dump_yaml(a, "test_a.yaml")