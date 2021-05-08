#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import urllib
import urllib2
import json
import sys
from check_notification import get_yesterday

az_url = "http://hadoop102:8081/"
az_username = "atguigu"
az_password = "atguigu"
project = "gmall"
flow = "gmall"


def post(url, data):
    """
    发送post请求到指定网址

    :param url: 指定网址
    :param data: 请求参数
    :return: 请求结果
    """
    body = urllib.urlencode(data)
    request = urllib2.Request(url, body)
    urlopen = urllib2.urlopen(request).read().decode('utf-8')
    return json.loads(urlopen)


def get(url, data):
    """
    发送get请求到指定网址

    :param url: 指定网址
    :param data: 请求参数
    :return: 请求结果
    """
    body = urllib.urlencode(data)
    urlopen = urllib2.urlopen(url + body).read().decode('utf-8')
    return json.loads(urlopen)


def login():
    """
    进行azkaban身份认证，并返回session ID

    :return: 返回session_id
    """
    data = {
        "action": "login",
        "username": az_username,
        "password": az_password
    }
    auth = post(az_url, data)
    return str(auth.get(u"session.id"))


def get_exec_id(session_id, project, flow):
    """
    获取正在执行的Flow的ExecId

    :param session_id: 和azkaban通讯的session_id
    :param project: 项目名称
    :param flow: 工作流名称
    :return: 执行ID
    """
    data = {
        "session.id": session_id,
        "ajax": "getRunning",
        "project": project,
        "flow": flow
    }
    execs = get(az_url + "executor?", data).get(u"execIds")
    if execs:
        return str(execs[0])
    else:
        return None


def wait_node(session_id, exec_id, node_id):
    """
    等待指定Flow中的一个节点执行完毕

    :param session_id: 和azkaban通讯的session_id
    :param exec_id: 执行ID
    :param node_id: 指定节点
    :return: 该节点是否成功执行完毕
    """
    data = {
        "session.id": session_id,
        "ajax": "fetchexecflow",
        "execid": exec_id
    }
    status = None
    while status not in ["SUCCEEDED", "FAILED", "CANCELLED", "SKIPPED"]:
        flow_exec = get(az_url + "executor?", data)
        for node in flow_exec.get(u"nodes"):
            if unicode(node_id) == node.get(u"id"):
                status = str(node.get(u"status"))
        print " ".join([node_id, status])
        time.sleep(1)
    return status == "SUCCEEDED"


def exec_flow(session_id, project_id, flow_id):
    """
    执行指定Flow

    :param session_id: 和azkaban通讯的session_id
    :param project_id: 指定的Project
    :param flow_id: 指定的Flow
    :return: 执行ID
    """
    data = {
        "session.id": session_id,
        "ajax": "executeFlow",
        "project": project_id,
        "flow": flow_id,
    }
    execs = post(az_url + "executor?", data)
    return str(execs.get(u"execid"))


def check_ods(dt, session_id, exec_id):
    """
    检查ODS层数据质量

    :param dt: 日期
    :param session_id: 和azkaban通讯的session_id
    :param exec_id: 指定的执行ID
    :return: None
    """
    if wait_node(session_id, exec_id, "hdfs_to_ods_db") and wait_node(session_id, exec_id, "hdfs_to_ods_log"):
        os.system("bash check_ods.sh " + dt)


def check_dim(dt, session_id, exec_id):
    """
    检查DIM层数据质量

    :param dt: 日期
    :param session_id: 和azkaban通讯的session_id
    :param exec_id: 指定的执行ID
    :return: None
    """
    if wait_node(session_id, exec_id, "ods_to_dim_db"):
        os.system("bash check_dim.sh " + dt)


def check_dwd(dt, session_id, exec_id):
    """
    检查DWD层数据质量

    :param dt: 日期
    :param session_id: 和azkaban通讯的session_id
    :param exec_id: 指定的执行ID
    :return: None
    """
    if wait_node(session_id, exec_id, "ods_to_dwd_db") and wait_node(session_id, exec_id, "ods_to_dwd_log"):
        os.system("bash check_dwd.sh " + dt)


if __name__ == '__main__':
    argv = sys.argv
    # 获取session_id
    session_id = login()

    # 获取执行ID。只有在原Flow正在执行时才能获取
    exec_id = get_exec_id(session_id, project, flow)

    # 获取日期，如果不存在取昨天
    if len(argv) >= 2:
        dt = argv[1]
    else:
        dt = get_yesterday()

    # 检查各层数据质量
    if exec_id:
        check_ods(dt, session_id, exec_id)
        check_dim(dt, session_id, exec_id)
        check_dwd(dt, session_id, exec_id)
