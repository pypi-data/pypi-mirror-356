pip 安装 pip install pythonDm

一个python调用大漠插件的库， 支持7.2450版本和3.1233版本的dm

7.2450 版本会获取管理员权限， 或者提前手动在程序属性里面设置管理员启动也可以。

7.2450版本需要 购买大漠插件的 vip注册码和附加码

3.1233版本可以免注册调用。这个版本是免费使用版本的最后版本。

"""
    导入方式：
    from PythonDm import *
    from PythonDm import Dm
    import PythonDm
"""

from PythonDm import Dm
import time


def test_create_dm_vip():
    dm = Dm(version=7, reg_code_append_key="your_key", reg_code="your_reg_code")
    while 1:
        print('循环中')
        time.sleep(1)


def test_create_dm_3():
    dm = Dm()
    while 1:
        print('循环中')
        time.sleep(1)

if __name__ == '__main__':
    test_create_dm_vip()




