# -*- coding: utf-8 -*-

"""
工具说明：一键设置 python 镜像，跨平台支持
author：sylan215
"""

import platform
import os


def write_to_file(filename):
    # 统一写入镜像配置信息
    with open(filename, 'w') as f_op:
        f_op.write('[global]\n')
        f_op.write('index-url = https://pypi.tuna.tsinghua.edu.cn/simple\n')
        f_op.write('[install]\n')
        f_op.write('trusted-host=http://mirrors.aliyun.com\n')
        f_op.write('\n')


def set_windows_mirror():
    # 设置 windows 环境的 python 镜像
    pip_dir = os.path.expanduser('~') + '\\pip'
    if not os.path.isdir(pip_dir):
        os.mkdir(pip_dir)
    pip_inf = pip_dir + '\\pip.ini'
    write_to_file(pip_inf)


def set_linux_mirror():
    # 设置 linux 环境的 python 镜像
    pip_dir = os.path.expanduser('~') + '/.pip'
    if not os.path.isdir(pip_dir):
        os.mkdir(pip_dir)
    pip_inf = pip_dir + '/pip.conf'
    write_to_file(pip_inf)


def set_mirror():
    # 获取操作系统类型
    os_name = platform.system()
    if os_name == "Windows":
        set_windows_mirror()
    else:
        set_linux_mirror()


if __name__ == "__main__":
    set_mirror()

