import calendar
import random
import string
import time
import uuid
import pymysql

from httprunner import __version__


db_user="test_rw"
db_password="Kyig&pnlGnaHaJ"
db_host="10.3.30.23"
db_port=3306


def get_httprunner_version():
    return __version__



def int_to_str(value):
    return str(value)


def str_to_int(value):
    try:
        return int(value)
    except:
        return None


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    """
    休眠n秒
    :param n_secs: 休眠的时间
    :return:
    """
    time.sleep(n_secs)


def gen_uuid4():
    """
    返回一个32位的uuid
    :return: 66e0efca-ce82-464b-935c-e12bf68850de
    """
    return str(uuid.uuid4())


def get_timestamp():
    """返回的是 1624521781324格式的时间戳"""
    return int(time.time() * 1000)


def get_time(type=2):
    """
    获取当前日期、时间
    :param type: 想要返回的时间类型
    :return: type=1,返回：Thu Jun 24 16:15:54 2021
             type=2,返回：2021-06-24 16:24:18
             type=3,返回：2021-06-24
             type=4,返回：16:37:23
    """
    if type == 1:
        return time.asctime(time.localtime())
    elif type == 2:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif type == 3:
        return time.strftime("%Y-%m-%d", time.localtime())
    elif type == 4:
        return time.strftime("%H:%M:%S", time.localtime())
    elif type == 5:
        return time.strftime("%Y%m%d%H%M%S", time.localtime())
    else:
        return "error time type"


def time_to_stamp(t):
    """
    将某个时间转时间戳
    :param t: 时间格式为："Sat Mar 28 22:24:24 2016",get_time(type=1)的返回值
    :return:返回时间戳
    """
    return time.mktime(time.strptime(t, "%a %b %d %H:%M:%S %Y"))


def print_calendar(type=0, year=2021, month=1):
    """
    日历相关的方法
    :param year: 想要获取的日历的年份
    :param month: 月份
    :param day: 日
    :return: type=0: 返回某年某月的日历
             type=1：返回某年一整年的日历
    """
    if type == 0:
        cal_month = calendar.month(year, month)
        return cal_month
    elif type == 1:
        cal_year = calendar.calendar(year, w=2, l=1, c=6)
        return cal_year


def is_leap(year):
    return calendar.isleap(year)


def random_number(num=None, start=0, end=9999999999):
    """
    在某一个范围内，随机生成一个数字
    :param start: 范围的起始数字
    :param end: 范围的结束数字
    :param num: 想要的数字位数
    :return: 返回一个随机数，返回的int类型
    """
    if num is None:
        return random.randint(start, end)
    else:
        id = ''.join(str(i) for i in random.sample(range(1, 9), num))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
        return int(id)


def random_number_str(num=None, start=0, end=9999999999):
    """
    在某一个范围内，随机生成一个数字
    :param start: 范围的起始数字
    :param end: 范围的结束数字
    :param num: 想要的数字位数
    :return: 返回一个随机数，返回的str类型
    """
    if num is None:
        return str(random.randint(start, end))
    else:
        id = ""
        for i in range(0, num):
            id += (str(random.randint(0,9)))
        # id = ''.join(str(i) for i in random.sample(range(0, 9), num))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
        return id



def random_str(amount):
    """
    返回随机字符串，大小写混合
    :param amount: 返回随机字符串的长度
    :return: 返回随机字符串
    """
    return "".join(random.sample(string.ascii_letters, amount))


def random_str_lower(amount):
    """
    返回随机字符串,全部小写字母
    :param amount: 返回随机字符串的长度
    :return: 返回随机字符串
    """
    return "".join(random.sample(string.ascii_letters, amount)).lower()


def random_str_upper(amount):
    """
    返回随机字符串,全部大写字母
    :param amount: 返回随机字符串的长度
    :return: 返回随机字符串
    """
    return "".join(random.sample(string.ascii_letters, amount)).upper()


def random_str_digit(amount):
    """
    返回随机字符串，内容包含字符和数字
    :param amount: 字符串的长度
    :return: 返回随机字符串，内容包含字符和数字
    """
    return "".join(random.sample(string.ascii_letters + string.digits, amount))


def random_str_sign(amount):
    """
    生成一个字母+数字+字符的随机数
    :param amount: 想要返回的随机数的长度
    :return: 返回一个随机字符串
    """
    str_list = []
    # sample = '0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()-+=.'
    sample = random.sample(
        string.ascii_letters + string.digits, 32
    )  ## 从a-zA-Z0-9生成指定数量的随机字符： list类型
    sample = sample + list("!@#$%^&*()-+=.")  # 原基础上加入一些符号元素
    for i in range(amount):
        char = random.choice(sample)  # 从sample中选择一个字符
        str_list.append(char)

    return "".join(str_list)  # 返回字符串


def random_char():
    """
    生成单个随机的字符
    :return:
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()"
    char = random.choice(alphabet)
    return char


def random_phone():
    """
    生成一个随机的手机号
    :return:
    """
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


def GBK2312():
    """
    随机返回一个汉字
    :return:
    """
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    st = bytes.fromhex(val).decode('gb2312')
    return st


def first_name():
    """
    随机取姓氏字典
    :return: 返回一个姓氏
    """
    first_name_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '易']
    n = random.randint(0, len(first_name_list) - 1)
    f_name = first_name_list[n]
    return f_name


def random_name():
    """
    随机生成2个或者3个汉字组成的名字，名字结尾会带一个test，比如：苏杨test
    :return:
    """
    n = random.randint(1, 2)
    name = ''
    for i in range(n):
        s = GBK2312()
        name = name + s
    return first_name() + name + 'test'


def random_email():
    """
    随机生成邮箱
    :return:
    """
    postfox = ['126.com', '163.com', 'gmail.com', 'sina.com', 'souhu.com']
    n = random.randint(0, len(postfox) - 1)
    email_postfox = postfox[n]
    n_pre = random.randint(4, 12)

    str_list = []
    # sample = '0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()-+=.'
    sample = random.sample(
        string.ascii_letters + string.digits, 32
    )  ## 从a-zA-Z0-9生成指定数量的随机字符： list类型

    sample = sample + list("_-.")  # 原基础上加入一些符号元素
    for i in range(n_pre):
        char = random.choice(sample)  # 从sample中选择一个字符
        str_list.append(char)

    str_email = "".join(str_list) +'@'+ email_postfox
    if n_pre % 2 ==0:
        return str_email# 返回字符串
    else:
        return random_qq_email()


def random_qq_email():
    """
    随机生成qq邮箱
    :return:
    """
    pre_email = random_number_str(None,10000000,9999999999)
    return pre_email + '@qq.com'


def assert_free(assert_param, param_dict):
    if isinstance(assert_param, int):
        assert_param = int_to_str(assert_param)
    if assert_param in param_dict.keys():
        return param_dict[assert_param]
    else:
        return assert_param


def connect_db(db_name, user=db_user, password=db_password, host=db_host, port=db_port, charset="utf8"):
    """
    连接数据库
    :param db_name: 数据库名字
    :param user: 登录数据库的用户名
    :param password: 数据库密码
    :param host: 数据库地址
    :param port: 数据库端口
    :param charset: 编码格式
    :return: 返回连接数据库的游标地址对象和数据库对象
    """
    conn = pymysql.connect(user=user,password=password,host=host,port=port,charset=charset)
    conn.select_db(db_name)
    cur = conn.cursor()
    return cur,conn


def close_db(cur, conn):
    """
    关闭游标和数据库
    :param cur: 游标对象
    :param conn: 数据库对象
    :return:
    """
    cur.close()
    conn.commit()
    conn.close()


def read_many_db_values(sql, db_name, charset="utf8"):
    """

    :param sql:
    :param db_name:
    :param charset:
    :return:
    """
    cur, conn = connect_db(db_name=db_name, charset=charset)
    # execute返回的是执行sql的条数
    cur.execute(sql)
    values = cur.fetchone()
    close_db(cur, conn)
    try:
        return values
    except TypeError:
        return None


def read_db_values(sql, db_name="inner_user", line = 1, charset="utf8"):
    """
    读数据库，sql查询出的结果含有多条数据
    :param sql: sql语句
    :param db_name: 数据库名字
    :param line: 数据行数，不想得到sql结果的全部数据，而是从游标处开始的前line行
    :param charset: 编码格式
    :return: 返回select查询到的结果
    """
    cur,conn = connect_db(db_name=db_name, charset=charset)
    # execute返回的是执行sql的条数
    cur.execute(sql)
    result = []
    if line:
        for i in range(0, line):
            result.append(cur.fetchmany(line))
    else:
        while True:
            res = cur.fetchone()
            if res is None:
                break
            result.append(res)

    close_db(cur, conn)
    return result


def read_db_value(sql, db_name="inner_user"):
    """
    读取数据库的某一个/行数据
    :param sql: sql语句
    :param db_name: 数据库名字
    :return: sql结果
    """
    cur, conn = connect_db(db_name=db_name)
    cur.execute(sql)
    value = cur.fetchone()
    close_db(cur, conn)
    try:
        return value[0]
    except TypeError:
        return None


def update_db_value(sql, db_name="inner_user"):
    """
    可以传一些
    :param sql: 更新、删除、添加的sql,更新或者删除的时候，务必要加where条件
    :param db_name: 需要操作的数据库
    :return:
    """
    try:
        cur, conn = connect_db(db_name=db_name)
        cur.execute(sql)
        close_db(cur, conn)
    except Exception:
        print("sql error")


def time_to_date():
    '''
    Created on 2015-4-14
    '''
    import datetime
    import time

    timeStamp = 1661159280000
    timeStamp /= 1000.0
    print(timeStamp)
    timearr = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
    print (otherStyleTime)


if __name__ == "__main__":
    # d = {'1464445729': "小青瓜", '5': "马旭广", '0': "null"}
    # value = assert_free_2("0", **d)
    # value = str_to_int('122')
    # value = assert_free('5', '1464445729-小青瓜#5-马旭广#0-null')
    # value = random_email()
    # print(value)
    # sql = "select eff_status from user_account where user_account_id=1499164073;"
    # value = read_db_value(sql, db_name="inner_user")
    # print(value)
    #
    # select_doctor_id = "select doctorId from glk_doctor_list where doctorName='茅斗test'"
    # # value = read_db_value(select_doctor_id, db_name="center")
    # value = read_db_value(select_doctor_id)
    # print(value)
    # print(random_number(num = 4))
    # print(random.randint(0, 9))
    # print(random_email())
    # sql = "update user_account set email='test1@medbanks.cn' where user_account_id=1"
    # update_db_value(sql)
    #
    value = time_to_date()
    print(value)
    #
    #
    #
