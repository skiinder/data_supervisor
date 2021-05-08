#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import check_all


if __name__ == '__main__':
    argv = sys.argv
    # 获取session_id
    session_id = check_all.login()

    # 获取执行ID。只有在原Flow正在执行时才能获取
    exec_id = check_all.get_exec_id(session_id, check_all.project, check_all.flow)

    # 获取日期，如果不存在取昨天
    if len(argv) >= 2:
        dt = argv[1]
    else:
        dt = check_all.get_yesterday()

    # 检查各层数据质量
    if exec_id:
        check_all.check_dwd(dt, session_id, exec_id)