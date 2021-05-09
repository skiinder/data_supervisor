#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
import json

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


def get_exec_id(session_id):
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
    while status not in ["SUCCEEDED", "FAILED", "CANCELLED", "SKIPPED", "KILLED"]:
        flow_exec = get(az_url + "executor?", data)
        for node in flow_exec.get(u"nodes"):
            if unicode(node_id) == node.get(u"id"):
                status = str(node.get(u"status"))
        print " ".join([node_id, status])
        time.sleep(1)
    return status == "SUCCEEDED"
