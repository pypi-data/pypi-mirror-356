# -*- coding: utf-8 -*-
# @Time    : 2025/6/17 下午2:33
# @Author  : 车小炮
"""
2025.06.17, 复制了Cycle_spider的func

"""

import asyncio
import datetime
import functools
import hashlib
import json
import pickle
import re
import pytz
import time
import traceback
from functools import wraps, partial
from pprint import pformat
from urllib.parse import urlencode
from loguru import logger as log
from w3lib.url import canonicalize_url as _canonicalize_url


def delay_time(wait_time):
    time.sleep(wait_time)


def format_seconds(seconds):
    """
    @summary: 将秒转为时分秒
    ---------
    @param seconds:
    ---------
    @result: 2天3小时2分49秒
    """

    seconds = int(seconds + 0.5)  # 向上取整

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    times = ""
    if d:
        times += "{}天".format(d)
    if h:
        times += "{}小时".format(h)
    if m:
        times += "{}分".format(m)
    if s:
        times += "{}秒".format(s)

    return times


def get_current_timestamp():
    return int(time.time())


def key2hump(key):
    """
    下划线试变成首字母大写
    """
    return key.title().replace("_", "")


# 异常捕捉
def run_safe_model(module_name):
    def inner_run_safe_model(func):
        try:

            @functools.wraps(func)  # 将函数的原来属性付给新函数
            def run_func(*args, **kw):
                callfunc = None
                try:
                    callfunc = func(*args, **kw)
                except Exception as e:
                    log.error(module_name + ": " + func.__name__ + " - " + str(e))
                    traceback.print_exc()
                return callfunc

            return run_func
        except Exception as e:
            log.error(module_name + ": " + func.__name__ + " - " + str(e))
            traceback.print_exc()
            return func

    return inner_run_safe_model


def get_info(text, regexs, allow_repeat=True, fetch_one=False, split=None):
    """
    正则表达式查找
    :param text: 内容
    :param regexs: 正则表达式， 可以是列表
    :param fetch_one: 是否获取，匹配的第一个
    :param allow_repeat: 仅在fetch_one=False时生效，是否允许结果重复
    :param split: 仅在fetch_one=False时生效，将结果拼接成str的分隔符，为None时不拼接
    :return:
    """
    _regexs = {}
    regexs = isinstance(regexs, str) and [regexs] or regexs
    infos = []
    for regex in regexs:
        if regex == "":
            continue

        if regex not in _regexs.keys():
            _regexs[regex] = re.compile(regex, re.S)

        if fetch_one:
            infos = _regexs[regex].search(text)
            if infos:
                infos = infos.groups()
            else:
                continue
        else:
            infos = _regexs[regex].findall(str(text))

        if len(infos) > 0:
            # print(regex)
            break

    if fetch_one:
        infos = infos if infos else ("",)
        return infos if len(infos) > 1 else infos[0]
    else:
        infos = allow_repeat and infos or sorted(set(infos), key=infos.index)
        infos = split.join(infos) if split else infos
        return infos


def dumps_obj(obj):
    return pickle.dumps(obj)


def loads_obj(obj_str):
    return pickle.loads(obj_str)


def key2underline(key: str, strict=True):
    """
    >>> key2underline("HelloWord")
    'hello_word'
    >>> key2underline("SHData", strict=True)
    's_h_data'
    >>> key2underline("SHData", strict=False)
    'sh_data'
    >>> key2underline("SHDataHi", strict=False)
    'sh_data_hi'
    >>> key2underline("SHDataHi", strict=True)
    's_h_data_hi'
    >>> key2underline("dataHi", strict=True)
    'data_hi'
    """
    regex = "[A-Z]*" if not strict else "[A-Z]"
    capitals = re.findall(regex, key)

    if capitals:
        for capital in capitals:
            if not capital:
                continue
            if key.startswith(capital):
                if len(capital) > 1:
                    key = key.replace(
                        capital, capital[:-1].lower() + "_" + capital[-1].lower(), 1
                    )
                else:
                    key = key.replace(capital, capital.lower(), 1)
            else:
                if len(capital) > 1:
                    key = key.replace(capital, "_" + capital.lower() + "_", 1)
                else:
                    key = key.replace(capital, "_" + capital.lower(), 1)

    return key.strip("_")


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ")", data_str)
    return data_str


def format_sql_value(value):
    if isinstance(value, str):
        value = value.strip()

    elif isinstance(value, (list, dict)):
        value = dumps_json(value, indent=None)

    elif isinstance(value, (datetime.date, datetime.time)):
        value = str(value)

    elif isinstance(value, bool):
        value = int(value)

    return value


def make_insert_sql(table, data, auto_update=False, update_columns=(), insert_ignore=False):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param insert_ignore: 数据存在忽略
    ---------
    @result:
    """

    keys = ["`{}`".format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", "")

    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        update_columns_ = ", ".join(
            ["{key}=values({key})".format(key=key) for key in update_columns]
        )
        sql = (
                "insert%s into `{table}` {keys} values {values} on duplicate key update %s"
                % (" ignore" if insert_ignore else "", update_columns_)
        )

    elif auto_update:
        sql = "replace into `{table}` {keys} values {values}"
    else:
        sql = "insert%s into `{table}` {keys} values {values}" % (
            " ignore" if insert_ignore else ""
        )

    sql = sql.format(table=table, keys=keys, values=values).replace("None", "null")
    return sql


def make_batch_sql(table, datas, auto_update=False, update_columns=(), update_columns_value=()):
    """
    @summary: 生产批量的sql
    ---------
    @param table:
    @param datas: 表数据 [{...}]
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param update_columns_value: 需要更新的列的值 默认为datas里边对应的值, 注意 如果值为字符串类型 需要主动加单引号， 如 update_columns_value=("'test'",)
    ---------
    @result:
    """
    if not datas:
        return

    keys = list(datas[0].keys())
    values_placeholder = ["%s"] * len(keys)

    values = []
    for data in datas:
        value = []
        for key in keys:
            current_data = data.get(key)
            current_data = format_sql_value(current_data)

            value.append(current_data)

        values.append(value)

    keys = ["`{}`".format(key) for key in keys]
    keys = list2str(keys).replace("'", "")

    values_placeholder = list2str(values_placeholder).replace("'", "")

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        if update_columns_value:
            update_columns_ = ", ".join(
                [
                    "`{key}`={value}".format(key=key, value=value)
                    for key, value in zip(update_columns, update_columns_value)
                ]
            )
        else:
            update_columns_ = ", ".join(
                ["`{key}`=values(`{key}`)".format(key=key) for key in update_columns]
            )
        sql = "insert into `{table}` {keys} values {values_placeholder} on duplicate key update {update_columns}".format(
            table=table,
            keys=keys,
            values_placeholder=values_placeholder,
            update_columns=update_columns_,
        )
    elif auto_update:
        sql = "replace into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )
    else:
        sql = "insert ignore into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )

    return sql, values


def make_update_sql(table, data, condition):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param condition: where 条件
    ---------
    @result:
    """
    key_values = []

    for key, value in data.items():
        value = format_sql_value(value)
        if isinstance(value, str):
            key_values.append("`{}`={}".format(key, repr(value)))
        elif value is None:
            key_values.append("`{}`={}".format(key, "null"))
        else:
            key_values.append("`{}`={}".format(key, value))

    key_values = ", ".join(key_values)

    sql = "update `{table}` set {key_values} where {condition}"
    sql = sql.format(table=table, key_values=key_values, condition=condition)
    return sql


def ensure_int(n):
    """
    >>> ensure_int(None)
    0
    >>> ensure_int(False)
    0
    >>> ensure_int(12)
    12
    >>> ensure_int("72")
    72
    >>> ensure_int('')
    0
    >>> ensure_int('1')
    1
    """
    if not n:
        return 0
    return int(n)


def aio_wrap(loop=None, executor=None):
    """
    wrap a normal sync version of a function to an async version
    """
    outer_loop = loop
    outer_executor = executor

    def wrap(fn):
        @wraps(fn)
        async def run(*args, loop=None, executor=None, **kwargs):
            if loop is None:
                if outer_loop is None:
                    loop = asyncio.get_event_loop()
                else:
                    loop = outer_loop
            if executor is None:
                executor = outer_executor
            pfunc = partial(fn, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)

        return run

    return wrap


def ensure_float(n):
    """
    >>> ensure_float(None)
    0.0
    >>> ensure_float(False)
    0.0
    >>> ensure_float(12)
    12.0
    >>> ensure_float("72")
    72.0
    """
    if not n:
        return 0.0
    return float(n)


def get_json(json_str):
    """
    @summary: 取json对象
    ---------
    @param json_str: json格式的字符串
    ---------
    @result: 返回json对象
    """

    try:
        return json.loads(json_str) if json_str else {}
    except Exception as e1:
        try:
            json_str = json_str.strip()
            json_str = json_str.replace("'", '"')
            keys = get_info(json_str, "(\w+):")
            for key in keys:
                json_str = json_str.replace(key, '"%s"' % key)

            return json.loads(json_str) if json_str else {}

        except Exception as e2:
            log.error(
                """
                e1: %s
                format json_str: %s
                e2: %s
                """
                % (e1, json_str, e2)
            )

        return {}


def jsonp2json(jsonp):
    """
    将jsonp转为json
    @param jsonp: jQuery172013600082560040794_1553230569815({})
    @return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", jsonp, re.S).group(1))
    except:
        raise ValueError("Invalid Input")


def dumps_json(data, indent=None, sort_keys=False):
    """
    @summary: 将json对象转化str
    ---------
    @param data: json格式的字符串或json对象
    :param sort_keys: 是否对key排序
    :param indent: 格式化，一个缩进级别0只会插入换行符。“None”是最简洁的表示，4表示4个空格缩进
    ---------
    @result: 格式化后的字符串
    """
    try:
        if isinstance(data, str):
            data = get_json(data)

        data = json.dumps(
            data,
            ensure_ascii=False,
            indent=indent,
            skipkeys=True,
            sort_keys=sort_keys,
            default=str,
        )

    except Exception as e:
        data = pformat(data)

    return data


def get_md5(*args):
    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_cookies_from_str(cookie_str):
    """
    >>> get_cookies_from_str("key=value; key2=value2; key3=; key4=; ")
    {'key': 'value', 'key2': 'value2', 'key3': '', 'key4': ''}

    Args:
        cookie_str: key=value; key2=value2; key3=; key4=

    Returns:

    """
    cookies = {}
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        key, value = cookie.split("=", 1)
        key = key.strip()
        value = value.strip()
        cookies[key] = value

    return cookies


def canonicalize_url(url):
    """
    url 归一化 会参数排序 及去掉锚点
    """
    return _canonicalize_url(url)


def cookies2str(cookies):
    str_cookie = ""
    for k, v in cookies.items():
        str_cookie += k
        str_cookie += "="
        str_cookie += v
        str_cookie += "; "
    return str_cookie


def joint_url(url, params):
    # param_str = "?"
    # for key, value in params.items():
    #     value = isinstance(value, str) and value or str(value)
    #     param_str += key + "=" + value + "&"
    #
    # return url + param_str[:-1]

    if not params:
        return url

    params = urlencode(params)
    separator = "?" if "?" not in url else "&"
    return url + separator + params


def transform_lower_num(data_str: str):
    """
    处理一二三……中文时间
    :param data_str:
    :return:
    """
    num_map = {
        "一": "1",
        "二": "2",
        "两": "2",
        "三": "3",
        "四": "4",
        "五": "5",
        "六": "6",
        "七": "7",
        "八": "8",
        "九": "9",
        "十": "0",
    }
    pattern = f'[{"|".join(num_map.keys())}|零]'
    res = re.search(pattern, data_str)
    if not res:
        #  如果字符串中没有包含中文数字 不做处理 直接返回
        return data_str

    data_str = data_str.replace("0", "零")
    for n in num_map:
        data_str = data_str.replace(n, num_map[n])

    re_data_str = re.findall("\d+", data_str)
    for i in re_data_str:
        if len(i) == 3:
            new_i = i.replace("0", "")
            data_str = data_str.replace(i, new_i, 1)
        elif len(i) == 4:
            new_i = i.replace("10", "")
            data_str = data_str.replace(i, new_i, 1)
        elif len(i) == 2 and int(i) < 10:
            new_i = int(i) + 10
            data_str = data_str.replace(i, str(new_i), 1)
        elif len(i) == 1 and int(i) == 0:
            new_i = int(i) + 10
            data_str = data_str.replace(i, str(new_i), 1)

    return data_str.replace("零", "0")


def format_date(date, old_format="", new_format="%Y-%m-%d %H:%M:%S"):
    """
    @summary: 格式化日期格式  2021年4月17日 3时27分12秒  ->  2021-04-17 03:27:12
    ---------
    @param date: 日期 eg：2021年4月17日 3时27分12秒
    @param old_format: 原来的日期格式 如 '%Y年%m月%d日 %H时%M分%S秒'
        %y 两位数的年份表示（00-99）
        %Y 四位数的年份表示（000-9999）
        %m 月份（01-12）
        %d 月内中的一天（0-31）
        %H 24小时制小时数（0-23）
        %I 12小时制小时数（01-12）
        %M 分钟数（00-59）
        %S 秒（00-59）
    @param new_format: 输出的日期格式
    ---------
    @result: 格式化后的日期，类型为字符串 如2017-4-17 03:27:12
    """
    if not date:
        return ""

    if not old_format:
        regex = "(\d+)"
        numbers = re.compile(regex, re.S).findall(str(date))
        formats = ["%Y", "%m", "%d", "%H", "%M", "%S"]
        old_format = date
        for i, number in enumerate(numbers[:6]):
            if i == 0 and len(number) == 2:  # 年份可能是两位 用小%y
                old_format = old_format.replace(
                    number, formats[i].lower(), 1
                )  # 替换一次 '2017年11月30日 11:49' 防止替换11月时，替换11小时
            else:
                old_format = old_format.replace(number, formats[i], 1)  # 替换一次

    try:
        date_obj = datetime.datetime.strptime(date, old_format)
        if "T" in date and "Z" in date:
            date_obj += datetime.timedelta(hours=8)
            date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_str = datetime.datetime.strftime(date_obj, new_format)

    except Exception as e:
        raise Exception("日期格式化出错，old_format = %s 不符合 %s 格式" % (old_format, date))
        # print("日期格式化出错，old_format = %s 不符合 %s 格式" % (old_format, date))
        # date_str = date

    return date_str


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(date_format)


def get_calculation_date(date_format="%Y-%m-%d %H:%M:%S", add_day=0):
    return (datetime.date.today() + datetime.timedelta(days=add_day)).strftime(date_format)

def get_calculation_shanghai_date(date_format="%Y-%m-%d %H:%M:%S", add_day=0):
    shanghai_date = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    return (shanghai_date + datetime.timedelta(days=add_day)).strftime(date_format)

def format_time(release_time, date_format="%Y-%m-%d %H:%M:%S"):
    """
    eg: format_time("2个月前")
    '2021-08-15 16:24:21'
    eg: format_time("2月前")
    '2021-08-15 16:24:36'
    """
    release_time = transform_lower_num(release_time)
    release_time = release_time.replace("日", "天").replace("/", "-")

    if "年前" in release_time:
        years = re.compile("(\d+)\s*年前").findall(release_time)
        years_ago = datetime.datetime.now() - datetime.timedelta(
            days=int(years[0]) * 365
        )
        release_time = years_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "月前" in release_time:
        months = re.compile("(\d+)[\s个]*月前").findall(release_time)
        months_ago = datetime.datetime.now() - datetime.timedelta(
            days=int(months[0]) * 30
        )
        release_time = months_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "周前" in release_time:
        weeks = re.compile("(\d+)\s*周前").findall(release_time)
        weeks_ago = datetime.datetime.now() - datetime.timedelta(days=int(weeks[0]) * 7)
        release_time = weeks_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "天前" in release_time:
        ndays = re.compile("(\d+)\s*天前").findall(release_time)
        days_ago = datetime.datetime.now() - datetime.timedelta(days=int(ndays[0]))
        release_time = days_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "小时前" in release_time:
        nhours = re.compile("(\d+)\s*小时前").findall(release_time)
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=int(nhours[0]))
        release_time = hours_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "分钟前" in release_time:
        nminutes = re.compile("(\d+)\s*分钟前").findall(release_time)
        minutes_ago = datetime.datetime.now() - datetime.timedelta(
            minutes=int(nminutes[0])
        )
        release_time = minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

    elif "前天" in release_time:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=2)
        release_time = release_time.replace("前天", str(yesterday))

    elif "昨天" in release_time:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        release_time = release_time.replace("昨天", str(yesterday))

    elif "今天" in release_time:
        release_time = release_time.replace("今天", get_current_date("%Y-%m-%d"))

    elif "刚刚" in release_time:
        release_time = get_current_date()

    elif re.search("^\d\d:\d\d", release_time):
        release_time = get_current_date("%Y-%m-%d") + " " + release_time

    elif not re.compile("\d{4}").findall(release_time):
        month = re.compile("\d{1,2}").findall(release_time)
        if month and int(month[0]) <= int(get_current_date("%m")):
            release_time = get_current_date("%Y") + "-" + release_time
        else:
            release_time = str(int(get_current_date("%Y")) - 1) + "-" + release_time

    # 把日和小时粘在一起的拆开
    template = re.compile("(\d{4}-\d{1,2}-\d{2})(\d{1,2})")
    release_time = re.sub(template, r"\1 \2", release_time)
    release_time = format_date(release_time, new_format=date_format)

    return release_time


def get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        log.error("Method %r not found in: %s" % (name, obj))
        return None


def print_key_val(key_, value, pre_indent=0, end=','):
    """将key和value，并将其插入代码列表中
    """
    indent = 4 * pre_indent
    code = ["{i}{s}'{v}'".format(i=" " * indent, s=key_, v=value)]
    code[-1] += end
    return code


def dict_to_code(name, simple_dict, pre_indent=0):
    indent = 4 * pre_indent
    code = []
    if simple_dict:
        code.append("{i}{name} = {{".format(i=" " * indent, name=name))
        # check for python3
        try:
            for k, v in simple_dict.items():
                init = "'{k}': ".format(k=k)
                code += print_key_val(init, v, pre_indent + 1)
        except:
            for k, v in simple_dict.iteritems():
                init = "'{k}': ".format(k=k)
                code += print_key_val(init, v, pre_indent + 1)
        code.append(" " * indent + "}")
    return code


def create_request(url, method, cookies, headers, data=None):
    """从参数创建request请求代码
    >>> code = create_request("https://localhost:8080", None, "get", None, None)
    """
    code = []
    code += dict_to_code("cookies", cookies)
    code += dict_to_code("headers", headers)
    code += print_key_val("url = ", url, end='')
    resstr = "res = requests.{}(url, ".format(method)
    append = "headers=headers"
    if cookies:
        append += ", cookies=cookies"
    if data:
        code.append("data = {}".format(data))
        if "application/json" in headers.get('Accept'):
            append += ", json=data"
        else:
            append += ", data=data"
    code.append(resstr + append + ")")
    code.append("print(res.text)\n")
    return code

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]


if __name__ == '__main__':
    # print(make_batch_sql({"biaoqiangbao": [{"asd": "yier", "bubu": "hapi", "ff": 124, "fasd": None},
    #                                        {"asd": "yier", "bubu": "hapi", "ff": 124, "fasd": None}]}))
    # cmd = """"""
    # print(curl_2_spider(cmd=cmd, type_='spider'))
    pass
