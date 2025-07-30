from .pydm import Dm
import inspect
import sys
__version__ = '1.1.0'  # 确保 在python调用库时候可以 查看这个库的版本号， 同时会被setup.py导入引用。


# 自动收集所有不以_开头的函数     这些会让这个包 可以用 from PythonDm import * 时候可以 导入包的所有内容。

__all__ = [name for name, obj in inspect.getmembers(sys.modules[__name__])
           if not name.startswith('_') and (inspect.isfunction(obj) or inspect.isclass(obj))]



