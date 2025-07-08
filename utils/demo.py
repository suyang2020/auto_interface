import requests
from datetime import datetime
import json

url = "https://app.work.weixin.qq.com/wework_admin/approval/api/get_approval_list"

headers = {
    "content-type": "application/x-www-form-urlencoded"
}

cookies = {
    "mp_version": "24889",
    "sid": "3B2EDEA0C9ED9352419CE0AD58DDA3D3C51118C9088CAAA99DF2A82DA06A1F7BFF8FD9CE7ADE9C088B5590EDED561F2712100A27B9F332AD91E22063B25B3500",
    "vid": "1688855622755902",
    "skey": "XGAfr94lTsqjd9io6x4pcgAA",
    "gid": "2251803514825021"
}

# 计算加班时间
def parse_time(time_str):
    """从字符串中解析时间（格式：2025/3/18 17:20）"""
    return datetime.strptime(time_str, "%Y/%m/%d %H:%M")


def calculate_overtime_hours(summary_list):
    """计算单个加班申请的时长（小时）"""
    start_time_str = None
    end_time_str = None

    # 从summary_list中提取开始时间和结束时间
    for item in summary_list:
        if item.startswith("开始时间："):
            start_time_str = item.replace("开始时间：", "").strip()
        elif item.startswith("结束时间："):
            end_time_str = item.replace("结束时间：", "").strip()

    if start_time_str and end_time_str:
        start_time = parse_time(start_time_str)
        end_time = parse_time(end_time_str)
        duration = end_time - start_time
        return duration.total_seconds() / 3600  # 转换为小时
    return 0


try:
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        # 将响应内容转换为字典
        response_dict = response.json()

        # 提取加班申请数据
        overtime_applications = response_dict.get("data", {}).get("xcxdata", [])

        total_overtime_hours = 0
        print("加班申请详情：")
        print("-" * 50)

        for app in overtime_applications:
            # 检查 lang_tp_names 中的 text 是否为 "加班"
            lang_tp_names = app.get("lang_tp_names", [])
            is_overtime = any(item.get("text") == "加班" for item in lang_tp_names)

            if not is_overtime:
                continue  # 如果不是加班申请，跳过

            sp_no = app.get("sp_no", "")
            apply_time = app.get("apply_time", "")
            summary_list = app.get("summary_list", [])
            overtime_hours = calculate_overtime_hours(summary_list)
            total_overtime_hours += overtime_hours

            # 将时间转换为字典格式
            time_info = {
                "申请单号": sp_no,
                "申请时间": datetime.fromtimestamp(apply_time).strftime('%Y-%m-%d %H:%M:%S') if apply_time else "",
                "事由": [s.replace("加班事由：", "") for s in summary_list if s.startswith("加班事由：")][
                    0] if summary_list else "",
                "开始时间": [s.replace("开始时间：", "") for s in summary_list if s.startswith("开始时间：")][
                    0] if summary_list else "",
                "结束时间": [s.replace("结束时间：", "") for s in summary_list if s.startswith("结束时间：")][
                    0] if summary_list else "",
                "加班时长（小时）": round(overtime_hours, 2)
            }

            # 打印字典格式的时间信息
            print(json.dumps(time_info, ensure_ascii=False, indent=2))
            print("-" * 50)

        print(f"总加班时长: {total_overtime_hours:.2f} 小时")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)

except requests.exceptions.RequestException as e:
    print("请求异常:", e)
except Exception as e:
    print("处理响应时出错:", e)