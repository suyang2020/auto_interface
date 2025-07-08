import pytest
import requests
from utils import times
import json
from utils.tools import message_to_wechat2
import csv
from config import conf


# 直播管理页面，创建直播，直播分享等


class TestLive:
    host = conf.HOST
    current_time = times.current_time()

    s = requests.session()
    live_id = ""
    live_record_id = ""
    live_cycle_record_id = ""
    material_id = conf.MATERIAL_ID   #素材ID

    def __init__(self, token):
        self.authorization = token


    def test_add_live(self):
        url = self.host + "/live/live/add"

        form_data = {
            "theme": "test_sy直播",
            "preOpenTime": self.current_time,
            "status": 0,
            "liveScreen": 2,
            "liveType": "1"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }


        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)
        else:
            print("创建直播成功")
            self.live_id = rep["data"]["id"]
            data = [[self.live_id]]
            with open('../files/live_id.csv', 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            return self.live_id

    def test_start_live(self, live_id):
        url = self.host + "/live/live/startLive"

        form_data = {
            "id": live_id
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }

        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)
        else:
            print("开启直播成功")

    def test_add_record_live(self):
        url = self.host + "/live/live/addRecordLive"

        form_data = {
            "goodsList": [],
                    "liveScreen": 2,
                    "theme": "test_sy循环伪直播",
                    "liveType": "2",
                    "materialId":self.material_id,
                    "preOpenTime": times.future_time(4),
                    "preEndTime": times.future_time(8),
                    "status": 0
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }

        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)

        else:
            print("创建循环伪直播成功")
            self.live_record_id = rep["data"]["id"]
            data = [[self.live_record_id]]
            with open('../files/live_record_id.csv', 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            return self.live_record_id

    def test_add_pre_record_live(self):
        url = self.host + "/live/live/addPreRecordLive"

        form_data = {

              "goodsList": [

              ],
              "theme": "test_sy伪直播",
              "preOpenTime": times.future_time(3),
              "preEndTime": times.future_time(13),
              "status": 0,
              "materialId": self.material_id,
              "liveScreen": 2,
              "liveType": "3"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }

        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)
        else:
            print("创建伪直播成功")
            self.live_cycle_record_id = rep["data"]["id"]
            data = [[self.live_cycle_record_id]]
            with open('../files/live_record_id.csv', 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            return self.live_cycle_record_id

    def test_live_sign(self,id_live=live_id):
        url = self.host + "/liveSign/liveSign/add"

        form_data = {
            "liveId": id_live,
            "title": "test签到",
            "startDate": times.future_time(3),
            "endDate": None,
            "endTime": 10,
            "tip": "sy签到提示",
            "buttonName": "签到按钮",
            "endTip": "结束提示",
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }

        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)

        else:
            print("新增签到成功")
            return rep["data"]["id"]


    def test_share_live(self, id_live):
        url = self.host + "/live/live/detail"

        params  = {
            "id": id_live
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }
        rep = self.s.get(
            url, params =params, headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": params, "rep": rep}
            message_to_wechat2(result)
        else:
            print("分享直播成功")
            share_url = rep["data"]["shareUrl"]
            push_url = rep["data"]["pushUrl"]
            pull_url = rep["data"]["pullUrl"]
            return share_url, push_url, pull_url

    def test_sign_list(self, id_live):
        url = self.host + "/liveSign/liveSign/page"

        params = {
            "liveId": id_live,
            "pageNum": 1,
            "pageSize": 10
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }
        rep = self.s.get(
            url, params=params, headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001" and rep["data"]["records"]["title"]!="test签到":
            result = {"url": url, "form_data": params, "rep": rep}
            message_to_wechat2(result)
        else:
            print("签到列表成功")


    def test_end_live(self, id_live):
        url = self.host + "/live/live/endLive"

        form_data = {
            "liveId": id_live,
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }
        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)
        else:
            print("关闭成功")

    def test_delete_live(self, id_live=live_id):
        url = self.host + "/live/live/delete"

        form_data = {
            "id": id_live
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=utf-8",
            "user-agent": "auto_interface_test",
            "authorization": self.authorization
        }

        rep = self.s.post(
            url, data=json.dumps(form_data).encode("utf-8"), headers=headers, verify=False
        )
        rep = json.loads(rep.content.decode("utf-8"))

        if rep['code'] != "20001":
            result = {"url": url, "form_data": form_data, "rep": rep}
            message_to_wechat2(result)
        else:
            print("删除直播成功")

#
# if __name__ == "__main__":
#     test_list = ["live_test.py"]
#     pytest.main(test_list)
