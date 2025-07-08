#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import xmltodict
import json
from utils import times
from config import conf
import xml.etree.ElementTree as ET
import os
from utils import logger


class JtlApi:

    def formatResultList(self, result_list):
        '''
        格式化结果List，去除多余的字符
        :param result_list:
        :return:
        '''
        result_new_list = list()
        for i in result_list:
            b = dict()
            for k, v in i.items():
                v = str(v).replace('\t', '')
                v = str(v).replace('\r', '')
                v = str(v).replace('\n', '')
                v = str(v).replace(' ', '')
                b[k] = v
            result_new_list.append(b)
        return result_new_list

    def jtlToList(self, jtl_file):
        '''
        jtl文件解析转成list对象
        :param jtl_file:
        :return:
        '''
        # tree = ET.ElementTree()  # 实例化
        # tree.parse(jtl_file)
        # root = tree.getroot()
        jtl_str = open(jtl_file, encoding="UTF-8").read()
        jtl_str = jtl_str.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        print(jtl_str)
        root = ET.fromstring(jtl_str)
        print(type(root))
        result_list = list()
        nums = 0
        for child in root:
            print(child)
            if "_" in child.get("lb"):
                nums = nums + 1
                data = dict()
                data["nums"] = 'STC%03d' % nums
                # data["name"] = child.get("lb")
                # data["scene"] = child.get("tn").split(' ')[0]
                names = child.get("lb").split("_")
                data["name"] = names[0]
                data["systemName"] = names[1]
                data["functionModule"] = names[2]
                data["result"] = child.get("s")
                for sub in child:
                    data[sub.tag] = sub.text
                result_list.append(data)
        result_list = self.formatResultList(result_list)
        return result_list

    def jtlToJson(self, jtl_file):
        '''
        jtl文件解析转成Json对象
        :param jtl_file:
        :return:
        '''
        xml_file = open(jtl_file, 'r', encoding='utf-8')
        xml_str = xml_file.read()
        xml_str = xml_str.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        converte_json = xmltodict.parse(xml_str, encoding='utf-8')
        json_str = json.dumps(converte_json, indent=4, ensure_ascii=False)

        try:
            json_object = json.loads(json_str)

            # 修改为更健壮的解析方式
            if "testResults" in json_object:
                temp = json_object["testResults"].get("httpSample", [])
                if not temp:  # 处理空结果情况
                    temp = json_object["testResults"].get("sample", [])
                # 如果jtl脚本只有一个，那temp就是一个字典，非列表，需要转成列表才能使用下面的方法
                if isinstance(temp, dict):
                    root = []
                    root.append(temp)
                else:
                    root = temp

        except Exception as e:
            logger.error(f"Error parsing JTL file: {str(e)}")
            return []

        result_list = list()
        nums = 0
        for child in root:
            nums = nums + 1
            data = dict()
            data["nums"] = 'STC%03d' % nums

            # 处理名称部分
            try:
                names = child.get("@lb", "").split("_")
                if len(names) == 3:
                    data["name"] = names[0]
                    data["systemName"] = names[2]
                    data["functionModule"] = names[1]
                else:
                    data["name"] = names[0] if names else ""
                    data["systemName"] = ""
                    data["functionModule"] = ""
            except AttributeError:
                data["name"] = ""
                data["systemName"] = ""
                data["functionModule"] = ""

            data["result"] = child.get("@s", "")

            # 安全获取可能不存在的字段
            def safe_get_text(node, key):
                item = node.get(key)
                return item.get("#text") if item and isinstance(item, dict) and "#text" in item else ""

            data["responseHeader"] = safe_get_text(child, "responseHeader")
            data["requestHeader"] = safe_get_text(child, "requestHeader")
            data["method"] = safe_get_text(child, "method")
            data["queryString"] = safe_get_text(child, "queryString")

            data["java.net.URL"] = child.get("java.net.URL", "")

            if 'responseData' in child:
                data["responseData"] = safe_get_text(child, "responseData")
            else:
                data["responseData"] = "/"

            result_list.append(data)

        result_list = self.formatResultList(result_list)
        return result_list

    def emailSummaryStatistics(self, result_list):
        '''
        邮件正文概要统计
        :param result_list:
        :return:
        '''
        fail_list = list()
        pass_nums = 0
        fail_nums = 0
        for result_dict in result_list:
            if result_dict.get("result").__contains__('true'):
                pass_nums = pass_nums + 1
            else:
                fail_nums = fail_nums + 1
                fail_list.append(result_dict.get("name"))

        try:
            pass_rate = str(round(pass_nums / (pass_nums + fail_nums) * 100, 2))
        except ZeroDivisionError:
            pass_rate = "0"
        email_result_dict = {
            "total": str(pass_nums + fail_nums),
            "passed": str(pass_nums),
            "failed": str(fail_nums),
            "pass_rate": pass_rate,
            "current_time": times.datetime_strftime("%Y-%m-%d %H:%M:%S"),
            # "fail_list": fail_list,
            "report_url": "https://www.medbanks.cn/"}
        return email_result_dict

    def reportDetailSummaryStatistics(self, result_list):
        '''
        报告详情概要统计
        :param result_list:
        :return:
        '''
        result_summary_dict = dict()
        for result_dict in result_list:
            if result_dict.get("result").__contains__('true'):
                scene = result_dict.get("systemName")
                if scene not in result_summary_dict.keys():
                    result_summary_dict[scene] = {'passed': 1, 'failed': 0}
                else:
                    passed = result_summary_dict[scene]['passed'] + 1
                    result_summary_dict[scene]['passed'] = passed
            else:
                scene = result_dict.get("systemName")
                if scene not in result_summary_dict.keys():
                    result_summary_dict[scene] = {'passed': 0, 'failed': 1}
                else:
                    failed = result_summary_dict[scene]['failed'] + 1
                    result_summary_dict[scene]['failed'] = failed
        for k, v in result_summary_dict.items():
            v['scene'] = k
            v['total'] = v.get('passed') + v.get('failed')
            v['pass_rate'] = str(round(v.get('passed') / v.get('total') * 100, 2))

        result_summary_html = str()
        with open(conf.RESULT_SUMMARY_TEMPLATE, encoding='utf-8') as f:
            content_html = f.read()
        for k, v in result_summary_dict.items():
            result_summary_html = result_summary_html + content_html.format(**v)
        return result_summary_html

    def reportDetailStatistics(self, result_list):
        '''
        报告详情统计
        :param result_list:
        :return:
        '''
        result_detail_html = str()
        with open(conf.RESULT_DETAIL_TEMPLATE, encoding='utf-8') as f:
            content_html = f.read()
        for result_detail_dict in result_list:
            url = result_detail_dict['java.net.URL']
            if "?" in url:
                url = url.split('?')[0]
            result_detail_dict['url'] = url
            result_detail_html = result_detail_html + content_html.format(**result_detail_dict)
        return result_detail_html

    def reportDetail(self, report_file, result_list):
        '''
        生成报告详情html页面
        :param report_file:
        :param result_list:
        :return:
        '''
        if os.path.exists(report_file):
            os.remove(report_file)

        result_summary_html = self.reportDetailSummaryStatistics(result_list)
        result_detail_html = self.reportDetailStatistics(result_list)
        report_dict = {'result_summary': result_summary_html,
                       'result_detail': result_detail_html,
                       'time': times.datetime_strftime("%Y-%m-%d %H:%M:%S")}
        with open(conf.REPORT_DETAIL_TEMPLATE, encoding='utf-8') as f:
            content_html = f.read()
        report_html = content_html.format(**report_dict)
        self.save_html(report_file, report_html)
        return report_html

    def save_html(self, report_file, report_html):
        with open(report_file, "wb") as f:
            f.write(bytes(report_html, 'UTF-8'))

    def indexReport(self, project_name_dict, index_report_file):
        '''
        生成index.html文件
        :param project_name_dict:  项目名称：{系统名称: 脚本名称}
        :param index_report_file:  文件名
        :return:
        '''
        if os.path.exists(index_report_file):
            os.remove(index_report_file)
        report_html_str = str()
        for project_name, system_name_dict in project_name_dict.items():
            rows = str(len(system_name_dict))
            num = 1
            for system_name, script_name in system_name_dict.items():
                if num == 1:
                    report_html_str = report_html_str + \
                                      '<tr valign="top">' \
                                      '<td rowspan="' + rows + '" align="center" valign="middle" style="background: #eeeee0;white-space: nowrap;"><span><b>' + project_name + '</b></span></td>' \
                                      '<td align="center" valign="middle" style="background: #eeeee0;white-space: nowrap;"><span><b>' + system_name + '</b></span></td>' \
                                      '<td align="center" style="background: #eeeee0;white-space: nowrap;"><span><b><a href="' + script_name + '_report.html">查看详情</a></b></span></td></tr>'
                else:
                    report_html_str = report_html_str +\
                                      '<td align="center" valign="middle" style="background: #eeeee0;white-space: nowrap;"><span><b>' + system_name + '</b></span></td>' \
                                      '<td align="center" style="background: #eeeee0;white-space: nowrap;"><span><b><a href="' + script_name + '_report.html">查看详情</a></b></span></td>' \
                                      '</tr>'
                num = num + 1
        index_dict = {'report_name': report_html_str,
                      'time': times.datetime_strftime("%Y-%m-%d %H:%M:%S")}
        with open(conf.INDEX_REPORT_TEMPLATE, encoding='utf-8') as f:
            content_html = f.read()
        index_report_html = content_html.format(**index_dict)
        self.save_html(index_report_file, index_report_html)

    # def xmlToJson(self, xml):
    #     xml_file = open(xml, 'r', encoding='utf-8')
    #     xml_str = xml_file.read();
    #     converte_json = xmltodict.parse(xml_str, encoding='utf-8')
    #     json_str = json.dumps(converte_json, indent=4, ensure_ascii=False)
    #     json_object = json.loads(json_str)
    #     return json_object
    #
    # def getAllCase(self, file):
    #     '''把jmeter执行结果jtl文件中的所有httpSample存放到一个list中'''
    #     caselist = []
    #     f = open(file, encoding='utf-8')
    #     for line in f.readlines():
    #         if line.startswith('<httpSample'):
    #             line = line[12:-2]
    #             caselist.append(line)
    #     # print('caselist', caselist)
    #     return caselist

    # def caselDicList(self, caselist):
    #     '''处理allcase，取出s,lb和rc作为字典存到list中'''
    #     casediclist = []  # 每条case是一个字典，把所有case存放到list里面
    #     # print(caselist)
    #     for case in caselist:
    #         # print(case)     #一条case，包含sample中的所有
    #         casedic = {}
    #         case_list = case.split(" ")
    #         for i in case_list:
    #             if i.__contains__("="):
    #                 key = i.split("=")[0]
    #                 casedic[key] = i.split("=")[1]
    #         casediclist.append(self.endCase(casedic))
    #     # print('casediclist', casediclist)
    #     return casediclist
    #
    # def endCase(self, casedic):
    #     """把casedic做处理，只保留s,lb,rc"""
    #     case_pre = casedic
    #     case_aft = {}
    #     for i in case_pre:
    #         if i == "s" or i == "lb" or i == "rc":
    #             case_aft[i] = case_pre.get(i)
    #     return case_aft
    #
    # def result_jtl(self, result_jtl_file):
    #     """分析结果"""
    #     casediclist = self.caselDicList(self.getAllCase(result_jtl_file))
    #     pass_nums = 0
    #     fail_nums = 0
    #     fail_list = []
    #     for casedic in casediclist:
    #         if casedic.get("s").__contains__('true'):
    #             pass_nums = pass_nums + 1
    #         else:
    #             fail_nums = fail_nums + 1
    #             fail_list.append(casedic.get("lb"))
    #
    #     result_dict = {
    #         "total": str(pass_nums + fail_nums),
    #         "passed": str(pass_nums),
    #         "failed": str(fail_nums),
    #         "pass_rate": str(round(pass_nums / (pass_nums + fail_nums) * 100, 2)),
    #         "current_time": times.datetime_strftime("%Y-%m-%d %H:%M:%S"),
    #         # "fail_list": fail_list,
    #         "report_url": "https://www.medbanks.cn/"
    #     }
    #     print(result_dict)
    #     send_mail.send_report(result_dict)


if __name__ == '__main__':
    # pass
    # jtl = JtlApi()
    # caselist = jtl.getAllCase(RESULT_DIR + '\\auto_test_user.jtl')  # 这里传入的是jtl的绝对路径
    # casediclist = jtl.caselDicList(jtl.getAllCase(RESULT_DIR + '\\auto_test_user.jtl'))
    # jtl.result(casediclist)
    jtl = JtlApi()
    # caselist = jtl.getAllCase(conf.RESULT_DIR + '\\auto_test_user.jtl')  # 这里传入的是jtl的绝对路径
    # casediclist = jtl.caselDicList(caselist)

    result_list = jtl.jtlToList(conf.RESULT_DIR + '\\auto_test_user.jtl')
    # email_result_list = jtl.emailSummaryStatistics(result_list)
    # print('email_result_list=== ', email_result_list)

    result_summary_html = jtl.reportDetailSummaryStatistics(result_list)
    # print('result_summary_dict=== ', result_summary_html)

    result_detail_html = jtl.reportDetailStatistics(result_list)
    # print('result_detail_html=== ', result_detail_html)

    report_html = jtl.reportDetail(result_summary_html, result_detail_html)
    print(report_html)
    report_file = conf.REPORT_DIR + "\\repot-" + times.datetime_strftime("%Y%m%d%H%M%S") + ".html"
    jtl.save_html(report_file, report_html)
