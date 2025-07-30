from PythonDm import Dm
import time


def test_create_dm_vip(reg_code, reg_code_append_key):
    """测试注册vpi"""
    dm = Dm(version=7, reg_code_append_key=reg_code_append_key, reg_code=reg_code)
    for i in range(5):
        print('循环中')
        time.sleep(1)
    input('任意键退出！！')


def test_create_dm_3():
    """ 测试注册 3版本 """
    dm = Dm()
    for i in range(5):
        print('循环中')
        time.sleep(1)
    input('任意键退出！！')


if __name__ == '__main__':
    test_create_dm_vip()



