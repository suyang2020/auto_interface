#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import shutil


def copydirs(from_file, to_file):
    if not os.path.exists(to_file):  # 如不存在目标目录则创建
        os.makedirs(to_file)
    files = os.listdir(from_file)  # 获取文件夹中文件和目录列表
    for f in files:
        if os.path.isdir(from_file + '/' + f):  # 判断是否是文件夹
            copydirs(from_file + '/' + f, to_file + '/' + f)  # 递归调用本函数
        else:
            shutil.copy(from_file + '/' + f, to_file + '/' + f)  # 拷贝文件


if __name__ == "__main__":
    pass
    # if os.path.exists(REPORT_TO_DIR):
    #     shutil.rmtree(REPORT_TO_DIR)
    #     print('删除成功')
    # shutil.copytree(REPORT_FROM_DIR, REPORT_TO_DIR)