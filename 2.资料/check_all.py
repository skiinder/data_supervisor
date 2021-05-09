#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from azclient import login, get_exec_id
from check_notification import get_yesterday
from check_dwd import check_dwd
from check_dim import check_dim
from check_ods import check_ods


if __name__ == '__main__':
    argv = sys.argv
    # 获取session_id
    session_id = login()

    # 获取执行ID。只有在原Flow正在执行时才能获取
    exec_id = get_exec_id(session_id)

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
