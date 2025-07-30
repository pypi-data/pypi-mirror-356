from .test_dm_reg import *
import inspect
import sys


# 自动收集所有不以_开头的函数
__all__ = [name for name, obj in inspect.getmembers(sys.modules[__name__])
           if not name.startswith('_') and (inspect.isfunction(obj) or inspect.isclass(obj))]