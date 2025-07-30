import win32com.client
import os
import ctypes
import subprocess
import sys
import win32com.client  # pip install pywin32==305
import time
import shutil


class Dm:
    def __init__(self, version=3, shell=False, dm_work_path='',  reg_code='', reg_code_append_key=''):
        """
            python调用大漠插件 兼容 7.2450   3.1233两个版本
            优化管理员模式注册大漠的 操作， 免注册模式可以使用3版本大漠
            通过shel= True 可以使用管理员模式注册大漠到系统。默认3版本是免注册调用，
            自动释放对应版本的dll文件到 大漠工作目录。这样再多给脚本同时调用这个库时候，他们就自己使用自己的大漠工作目录，而互相隔离。
            对于vip注册失败的情况 给出了详细的错误信息提示。
            如果打包后出现管理员权限不足情况: 可以  pyinstaller -F --uac-admin your_code.py 打包exe， exe可以自动在启动时候申请管理员权限。
        """
        self.version = version
        self.shell = shell
        self.dm_com = None
        self.dm_version = ""

        # 获取本文件的绝对路径
        self.current_file_path = os.path.abspath(__file__)
        # 获取本文件所在目录的绝对路径
        self.current_dir_path = os.path.dirname(self.current_file_path)
        # 根据本源码文件的所在目录 生辰 资源文件 DmReg.dll 的完整路径
        self.current_reg_dm_dll_path = os.path.join(self.current_dir_path, "dm", 'DmReg.dll')
        # 生成大漠工作目录：
        self.dm_work_path = dm_work_path or os.path.join(os.getcwd(), "dm" )
        # 生成大漠工作目录下的 DmReg.dll完整路径：
        self.dm_reg_dll_path = os.path.join(self.dm_work_path, "DmReg.dll")
        # 如果用户忘记填写 参数不完整，那么默认自动降级为 3版本运行。
        if self.version == 7 and (reg_code == '' or reg_code_append_key == ''):
            self.version = 3
            print('缺少注册码参数 自动降级为3版本大漠')

        if self.version == 7:
            self.dm_dll_path = os.path.join(self.dm_work_path, "dm.dll") # 大漠插件dm.dll文件路径
            self.current_dm_dll_path = os.path.join(self.current_dir_path, "dm", 'dm.dll')
            self.dm_version = '7.2450'
        elif self.version == 3:
            self.dm_dll_path = os.path.join(self.dm_work_path, "dm3.1233.dll")
            self.current_dm_dll_path = os.path.join(self.current_dir_path, "dm", 'dm3.1233.dll')
            self.dm_version = "3.1233"
        else:
            raise Exception('大漠版本参数错误')

        # 释放大漠插件文件：
        if not os.path.isdir(self.dm_work_path):
            os.mkdir(self.dm_work_path)
        if not os.path.isfile(self.dm_reg_dll_path):
            shutil.copy(self.current_reg_dm_dll_path, self.dm_reg_dll_path)
        if not os.path.isfile(self.dm_dll_path):
            shutil.copy(self.current_dm_dll_path, self.dm_dll_path)
        # 注册大漠到系统
        self._reg_dm_()

        # 检查版本号
        if self.dm_com.ver() == self.dm_version:
            print(f'注册大漠成功 {self.dm_com.ver()}')
        else:
            raise Exception('大漠对象创建失败')
        # 如果是调用新版 大漠 则注册vip  , 没有使用管理员模式启动时候 注册大漠vip提示-2 但是执行免费功能是有效的。
        self.reg_vip(reg_code, reg_code_append_key)
        # 初始化大漠：
        self.dm_com.SetPath(self.dm_work_path)  # 设置工作目录
        self.dm_com.SetShowErrorMsg(0)
        self.dm_com.SetDict(0, "dm_soft.txt")  # 设置字库
        # 加载 大漠com组件内的方法到 python 类
        self._add_methods(self.dm_com)

    def reg_vip(self, reg_code, reg_code_append_key):
        if not self.version == 7:
            return 0
        result = self.dm_com.Reg(reg_code, reg_code_append_key)
        print(' result=',  result)
        if result == 1:
            print('vip注册成功')
        elif result == -2:
            print('没有使用管理员方式注册 只能使用免费功能')
        if result == -1:
            raise Exception(f'大漠vip注册失败: {result}, 无法连接网络, (可能防火墙拦截, 如果可以正常访问大漠插件网站，那就可以肯定是被防'
                            f'火墙拦截)')
        elif result == 0:
            raise Exception(f'大漠vip注册失败: {result}, 失败(未知错误)')
        elif result == 2:
            raise Exception(f'大漠vip注册失败: {result}, 余额不足')
        elif result == 3:
            raise Exception(f'大漠vip注册失败: {result}, 绑定了本机器，但是账户余额不足50元.')
        elif result == 4:
            raise Exception(f'大漠vip注册失败: {result}, 注册码错误')
        elif result == 5:
            raise Exception(f'大漠vip注册失败: {result}, 你的机器或者IP在黑名单列表中或者不在白名单列表中.')
        elif result == 6:
            raise Exception(f'大漠vip注册失败: {result}, 非法使用插件.一般出现在定制插件时，使用了和绑定的用户名不同的注册码.也有可能是'
                            f'系统的语言设置不是中文简体, 也可能有这个错误.')
        elif result == 7:
            raise Exception(f'大漠vip注册失败: {result}, 你的帐号因为非法使用被封禁. （如果是在虚拟机中使用插件，必须使用Reg或者Re'
                f'gEx，不能使用RegNoMac或者RegExNoMac, 否则可能会造成封号，或者封禁机器）')
        elif result == 8:
            raise Exception(f'大漠vip注册失败: {result}, ver_info不在你设置的附加白名单中.')
        elif result == 77:
            raise Exception(f'大漠vip注册失败: {result}, 机器码或者IP因为非法使用，而被封禁. （如果是在虚拟机中使用插件，必须使用Re'
                f'g或者RegEx，不能使用RegNoMac或者RegExNoMac, 否则可能会造成封号，或者封禁机器）封禁是全局的，如果使用'
                f'了别人的软件导致77，也一样会导致所有注册码均无法注册。解决办法是更换IP，更换MAC.')
        elif result == 777:
            raise Exception(f'大漠vip注册失败: {result}, 同一个机器码注册次数超过了服务器限制,被暂时封禁. 请登录后台，插件今日详细消'
                f'费记录里，相应的机器码是否有次数异常，并立刻优化解决.如果还有问题，可以联系我来解决')
        elif result == -8:
            raise Exception(f'大漠vip注册失败: {result},  版本附加信息长度超过了32')
        elif result == -9:
            raise Exception(f'大漠vip注册失败: {result},  版本附加信息里包含了非法字母.')
        return 1

    def _reg_dm_(self):
        # 尝试管理员方式注册大漠对象
        if self.version == 7 or self.shell==True:
            try:
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    # 如果没有管理员权限：
                    for c in sys.argv:
                        if '二次启动' in c:
                            # 如果这已经是第二次重启自己仍然没有管理员权限 就停止运行 避免无限循环打开窗口。
                            input('启动失败 缺少管理员权限')
                            
                            exit()
                    # 如果是第一次启动没有管理员权限，就给自己的启动参数增加一个 二次启动 参数 ，以防止本次启动失败的话，下次继续无限循环
                    params = ' '.join(sys.argv)+ ' ' + '二次启动'
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)  # 0表示隐藏窗口
                    # 获取管理员重启自己之后，关闭当前没有管理员权限的进程。
                    exit()
                    
                # 管理员权限 或者提升权限后：
                # 执行命令并隐藏窗口
                subprocess.Popen(f"regsvr32  {self.dm_dll_path} /s", shell=True)
                self.dm_com = win32com.client.Dispatch('dm.dmsoft')
                # 如果管理员模式注册成功 函数结束了
            except Exception as e:
                # 捕捉管理员方式注册大漠的错误 如果捕捉到 就会继续执行调用 免注册模式
                print(e)
                obj = ctypes.windll.LoadLibrary(self.dm_reg_dll_path)
                obj.SetDllPathW(self.dm_dll_path, 0)
                self.dm_com = win32com.client.DispatchEx("dm.dmsoft")
        else:
            # 如果管理员方式注册失败则 尝试免注册调用大漠：
            obj = ctypes.windll.LoadLibrary(self.dm_reg_dll_path)
            obj.SetDllPathW(self.dm_dll_path, 0)
            self.dm_com = win32com.client.DispatchEx("dm.dmsoft")

    def _auto_com_to_class_fun(self, com_object):
        """ 获取 com组件内的所有方法 过滤掉内部方法（通常以单下划线开头）， 全部打印出来
            可以用于兼容更多版本的插件，构建get_all_fromdm_com 函数
        """
        code = ''
        for method in dir(com_object):
            if not method.startswith('_'):  # 过滤掉内部方法（通常以单下划线开头）
                code += f" self.{method} = self.dm_com.{method}\n"
        print( code )

    def _add_methods(self, com_object=None):
        """
            把com组件里面的所有方法全部 引用到当前类。
            这样也可以把所有方法动态加载到python 类中 但是写代码时候没有提示词，只有 遍历提前静态把所有方法赋值才可以
            # for method in dir(com_object):
            #     if not method.startswith('_'):  # 过滤掉内部方法（通常以单下划线开头）
            #         setattr(self, method, getattr(com_object, method))  # 将方法添加到类中
        """
        if self.version == 7:
            self.get_all_from_dm_com()
        elif self.version == 3:
            self.get_all_from_dm_com_3_1233()

    def move_to_left_click(self, x, y, wait_time=0.01, msg="", time_out=10):
        """ 大漠 移动鼠标到指定坐标后左键单机
            x, y: 坐标
            wait_time: 移动鼠标后 点击之前的延迟。默认10毫秒。
            msg: 点击后的 输出文字信息。
            time_out: 在鼠标点击之前会判断当前鼠标位置是否与目标位置一致，如果一致则点击，不一致则重新moveto。 超时10秒
        """
        start_time = time.time()
        while time.time()-start_time<time_out:
            self.dm_com.MoveTo(x, y)
            time.sleep(wait_time)
            if self._is_target_x_y_same(x, y):
                self.dm_com.LeftClick()
                break
            time.sleep(0.006)
        if msg:
            print(msg)

    def move_to_left_down_up(self, x, y, wait_time=0.01, down_time=0.03, msg="", time_out=10):
        """ 区别于 move_to_left_click 是：
         down_time： 左键按下弹起时间 这里可以自定义。
        """
        start_time = time.time()
        while time.time()-start_time<time_out:
            self.dm_com.MoveTo(x, y)
            time.sleep(wait_time)
            if self._is_target_x_y_same(x, y):
                self.dm_com.LeftDown()
                time.sleep(down_time)
                self.dm_com.LeftUp()
                break
            time.sleep(0.006)
        if msg:
            print(msg)

    def move_to_right_down_up(self, x, y, wait_time=0.01, down_time=0.03, msg="", time_out=10):
        """ 大漠 移动鼠标到指定坐标后右键单击
            区别于move_to_left_down_up： 这是右键操作
        """
        start_time = time.time()
        while time.time()-start_time<time_out:
            self.dm_com.MoveTo(x, y)
            time.sleep(wait_time)
            if self._is_target_x_y_same(x, y):
                self.dm_com.RightDown()
                time.sleep(down_time)
                self.dm_com.RightUp()
                break
            time.sleep(0.006)
        if msg:
            print(msg)

    def move_to_right_click(self, x, y, wait_time=0.01, msg="", time_out=10):
        """ 大漠 移动鼠标到指定坐标右键单击
            和 move_to_left_click 的区别 是： 这是右键操作 而非左键操作
        """
        start_time = time.time()
        while time.time() - start_time < time_out:
            self.dm_com.MoveTo(x, y)
            time.sleep(wait_time)
            if self._is_target_x_y_same(x, y):
                self.dm_com.RightClick()
                break
            time.sleep(0.006)
        if msg:
            print(msg)

    def _is_target_x_y_same(self, target_x, target_y):
        """ 内部方法 用于判断  当前鼠标 是否是 目标坐标"""
        for i in range(100):
            r, x, y = self.dm_com.GetCursorPos()
            if r == 1:
                if x == target_x and y == target_y:
                    return True
            else:
                time.sleep(0.001)
        return False

    def keydown_up_char(self, key, t):
        """  keydown up char 组合"""
        self.dm_com.KeyDownChar(key)
        time.sleep(t)
        self.dm_com.KeyUpChar(key)

    def keydown_up(self, key, t):
        """  keydown up code 组合"""
        self.dm_com.KeyDown(key)
        time.sleep(t)
        self.dm_com.KeyUp(key)

    def keypress_char_shortcut(self, char_first, char_and):
        """ 按下组合键 char"""
        self.dm_com.KeyDownChar(char_first)
        time.sleep(0.03)
        self.dm_com.KeyPressChar(char_and)
        time.sleep(0.03)
        self.dm_com.KeyUpChar(char_first)

    def keypress_shortcut(self, char_first, char_and):
        """ 按下组合键 code """
        self.dm_com.KeyDown(char_first)
        time.sleep(0.03)
        self.dm_com.KeyPress(char_and)
        time.sleep(0.03)
        self.dm_com.KeyUp(char_first)

    def find_pic(self, x1, y1, x2, y2, pic_name, sim=0.95,  ps="101010", fx=0, mode=1, timeout=0, e=""):
        if timeout:
            start_tm = int(time.time())
            # print("有超时设置")
        while True:
            dm_ret = self.dm_com.FindPicEx(x1, y1, x2, y2, pic_name, ps, sim, fx)
            if timeout:
                if dm_ret == "":
                    if int(time.time()) - start_tm >= timeout:
                        if e:
                            print(e)
                        # else:
                        #     # print("没有错误信息")
                    else:
                        time.sleep(0.1)
                        # print("继续找")
                        continue
                else:
                    # print("找到了")
                    pass
            # else:
            #     print("没有设置超时")
            if mode == 1:
                if dm_ret == "":
                    # print("没找到")
                    return -1, -1, -1
                else:
                    ls_tmp = dm_ret.split("|")
                    ls_ret = ls_tmp[0].split(",")
                    # print("找到了返回三个值")
                    # print(dm_ret)
                    return int(ls_ret[0]), int(ls_ret[1]), int(ls_ret[2])
            else:
                # print("返回字符串")
                return dm_ret

    def find_pic_ex(self, x1, y1, x2, y2, pic, ps, sim, fx):
        """大漠找图 改变了原本的返回值。"""
        str_dm_ret = self.dm_com.FindPicEx(x1, y1, x2, y2, pic, ps, sim, fx)
        if str_dm_ret:
            ls_str_dm_ret = str_dm_ret.split("|")
            dm_ret = ls_str_dm_ret[0].split(",")
            for index in range(3):
                dm_ret[index] = int(dm_ret[index])
        else:
            dm_ret = [-1, -1, -1]
        return dm_ret

    def while_find_pic(self, x1, y1, x2, y2, pic, ps='101010', sim=0.95, fx=0, time_out=20, pl=0.5, msg=''):
        ret, x, y = -1, -1, -1
        start_time = time.time()
        while time.time() - start_time <= time_out:
            ret, x, y = self.find_pic_ex(x1, y1, x2, y2, pic, ps, sim, fx)
            if ret > -1:
                if msg:
                    print(f'找到图片： [ {pic}]  返回值： {ret}, {x}, {y}', )
                break
            time.sleep(pl)
        if msg:
            print(f'没有找到图片： [ {pic}]    返回值： {ret}, {x}, {y}', )
        return ret, x, y

    def click_by_while_find_pic(self, x1, y1, x2, y2, pic, ps='101010', sim=0.95, fx=0, time_out=20, pl=0.5, msg='', wait=0, click_mode='long', down_time=0.1, e_print=True):
        ret, x, y = self.while_find_pic(x1, y1, x2, y2, pic, ps=ps, sim=sim, fx=fx, time_out=time_out, pl=pl)
        if ret > -1:
            if wait:
                time.sleep(wait)
            if click_mode=='long':
                self.move_to_left_down_up(x, y, down_time=down_time)
            else:
                self.move_to_left_click(x, y)
            if msg:
                print(f'点击 [{pic}] 操作成功：{msg}')
            return True
        else:
            if msg and e_print:
                print(f'点击 [{pic}] 操作失败：{msg}')
            return False

    def get_all_from_dm_com(self):
        """ 加载 7.2450版本大漠的全部公开方法 """
        self.ActiveInputMethod = self.dm_com.ActiveInputMethod
        self.AddDict = self.dm_com.AddDict
        self.AddRef = self.dm_com.AddRef
        self.AiEnableFindPicWindow = self.dm_com.AiEnableFindPicWindow
        self.AiFindPic = self.dm_com.AiFindPic
        self.AiFindPicEx = self.dm_com.AiFindPicEx
        self.AiFindPicMem = self.dm_com.AiFindPicMem
        self.AiFindPicMemEx = self.dm_com.AiFindPicMemEx
        self.AiYoloDetectObjects = self.dm_com.AiYoloDetectObjects
        self.AiYoloDetectObjectsToDataBmp = self.dm_com.AiYoloDetectObjectsToDataBmp
        self.AiYoloDetectObjectsToFile = self.dm_com.AiYoloDetectObjectsToFile
        self.AiYoloFreeModel = self.dm_com.AiYoloFreeModel
        self.AiYoloObjectsToString = self.dm_com.AiYoloObjectsToString
        self.AiYoloSetModel = self.dm_com.AiYoloSetModel
        self.AiYoloSetModelMemory = self.dm_com.AiYoloSetModelMemory
        self.AiYoloSetVersion = self.dm_com.AiYoloSetVersion
        self.AiYoloSortsObjects = self.dm_com.AiYoloSortsObjects
        self.AiYoloUseModel = self.dm_com.AiYoloUseModel
        self.AppendPicAddr = self.dm_com.AppendPicAddr
        self.AsmAdd = self.dm_com.AsmAdd
        self.AsmCall = self.dm_com.AsmCall
        self.AsmCallEx = self.dm_com.AsmCallEx
        self.AsmClear = self.dm_com.AsmClear
        self.AsmSetTimeout = self.dm_com.AsmSetTimeout
        self.Assemble = self.dm_com.Assemble
        self.BGR2RGB = self.dm_com.BGR2RGB
        self.Beep = self.dm_com.Beep
        self.BindWindow = self.dm_com.BindWindow
        self.BindWindowEx = self.dm_com.BindWindowEx
        self.Capture = self.dm_com.Capture
        self.CaptureGif = self.dm_com.CaptureGif
        self.CaptureJpg = self.dm_com.CaptureJpg
        self.CapturePng = self.dm_com.CapturePng
        self.CapturePre = self.dm_com.CapturePre
        self.CheckFontSmooth = self.dm_com.CheckFontSmooth
        self.CheckInputMethod = self.dm_com.CheckInputMethod
        self.CheckUAC = self.dm_com.CheckUAC
        self.ClearDict = self.dm_com.ClearDict
        self.ClientToScreen = self.dm_com.ClientToScreen
        self.CmpColor = self.dm_com.CmpColor
        self.CopyFile = self.dm_com.CopyFile
        self.CreateFolder = self.dm_com.CreateFolder
        self.CreateFoobarCustom = self.dm_com.CreateFoobarCustom
        self.CreateFoobarEllipse = self.dm_com.CreateFoobarEllipse
        self.CreateFoobarRect = self.dm_com.CreateFoobarRect
        self.CreateFoobarRoundRect = self.dm_com.CreateFoobarRoundRect
        self.DecodeFile = self.dm_com.DecodeFile
        self.DelEnv = self.dm_com.DelEnv
        self.Delays = self.dm_com.Delays
        self.DeleteFile = self.dm_com.DeleteFile
        self.DeleteFolder = self.dm_com.DeleteFolder
        self.DeleteIni = self.dm_com.DeleteIni
        self.DeleteIniPwd = self.dm_com.DeleteIniPwd
        self.DisAssemble = self.dm_com.DisAssemble
        self.DisableCloseDisplayAndSleep = self.dm_com.DisableCloseDisplayAndSleep
        self.DisableFontSmooth = self.dm_com.DisableFontSmooth
        self.DisablePowerSave = self.dm_com.DisablePowerSave
        self.DisableScreenSave = self.dm_com.DisableScreenSave
        self.DmGuard = self.dm_com.DmGuard
        self.DmGuardExtract = self.dm_com.DmGuardExtract
        self.DmGuardLoadCustom = self.dm_com.DmGuardLoadCustom
        self.DmGuardParams = self.dm_com.DmGuardParams
        self.DoubleToData = self.dm_com.DoubleToData
        self.DownCpu = self.dm_com.DownCpu
        self.DownloadFile = self.dm_com.DownloadFile
        self.EnableBind = self.dm_com.EnableBind
        self.EnableDisplayDebug = self.dm_com.EnableDisplayDebug
        self.EnableFakeActive = self.dm_com.EnableFakeActive
        self.EnableFindPicMultithread = self.dm_com.EnableFindPicMultithread
        self.EnableFontSmooth = self.dm_com.EnableFontSmooth
        self.EnableGetColorByCapture = self.dm_com.EnableGetColorByCapture
        self.EnableIme = self.dm_com.EnableIme
        self.EnableKeypadMsg = self.dm_com.EnableKeypadMsg
        self.EnableKeypadPatch = self.dm_com.EnableKeypadPatch
        self.EnableKeypadSync = self.dm_com.EnableKeypadSync
        self.EnableMouseAccuracy = self.dm_com.EnableMouseAccuracy
        self.EnableMouseMsg = self.dm_com.EnableMouseMsg
        self.EnableMouseSync = self.dm_com.EnableMouseSync
        self.EnablePicCache = self.dm_com.EnablePicCache
        self.EnableRealKeypad = self.dm_com.EnableRealKeypad
        self.EnableRealMouse = self.dm_com.EnableRealMouse
        self.EnableShareDict = self.dm_com.EnableShareDict
        self.EnableSpeedDx = self.dm_com.EnableSpeedDx
        self.EncodeFile = self.dm_com.EncodeFile
        self.EnterCri = self.dm_com.EnterCri
        self.EnumIniKey = self.dm_com.EnumIniKey
        self.EnumIniKeyPwd = self.dm_com.EnumIniKeyPwd
        self.EnumIniSection = self.dm_com.EnumIniSection
        self.EnumIniSectionPwd = self.dm_com.EnumIniSectionPwd
        self.EnumProcess = self.dm_com.EnumProcess
        self.EnumWindow = self.dm_com.EnumWindow
        self.EnumWindowByProcess = self.dm_com.EnumWindowByProcess
        self.EnumWindowByProcessId = self.dm_com.EnumWindowByProcessId
        self.EnumWindowSuper = self.dm_com.EnumWindowSuper
        self.ExcludePos = self.dm_com.ExcludePos
        self.ExecuteCmd = self.dm_com.ExecuteCmd
        self.ExitOs = self.dm_com.ExitOs
        self.FaqCancel = self.dm_com.FaqCancel
        self.FaqCapture = self.dm_com.FaqCapture
        self.FaqCaptureFromFile = self.dm_com.FaqCaptureFromFile
        self.FaqCaptureString = self.dm_com.FaqCaptureString
        self.FaqFetch = self.dm_com.FaqFetch
        self.FaqGetSize = self.dm_com.FaqGetSize
        self.FaqIsPosted = self.dm_com.FaqIsPosted
        self.FaqPost = self.dm_com.FaqPost
        self.FaqRelease = self.dm_com.FaqRelease
        self.FaqSend = self.dm_com.FaqSend
        self.FetchWord = self.dm_com.FetchWord
        self.FindColor = self.dm_com.FindColor
        self.FindColorBlock = self.dm_com.FindColorBlock
        self.FindColorBlockEx = self.dm_com.FindColorBlockEx
        self.FindColorE = self.dm_com.FindColorE
        self.FindColorEx = self.dm_com.FindColorEx
        self.FindData = self.dm_com.FindData
        self.FindDataEx = self.dm_com.FindDataEx
        self.FindDouble = self.dm_com.FindDouble
        self.FindDoubleEx = self.dm_com.FindDoubleEx
        self.FindFloat = self.dm_com.FindFloat
        self.FindFloatEx = self.dm_com.FindFloatEx
        self.FindInputMethod = self.dm_com.FindInputMethod
        self.FindInt = self.dm_com.FindInt
        self.FindIntEx = self.dm_com.FindIntEx
        self.FindMulColor = self.dm_com.FindMulColor
        self.FindMultiColor = self.dm_com.FindMultiColor
        self.FindMultiColorE = self.dm_com.FindMultiColorE
        self.FindMultiColorEx = self.dm_com.FindMultiColorEx
        self.FindNearestPos = self.dm_com.FindNearestPos
        self.FindPic = self.dm_com.FindPic
        self.FindPicE = self.dm_com.FindPicE
        self.FindPicEx = self.dm_com.FindPicEx
        self.FindPicExS = self.dm_com.FindPicExS
        self.FindPicMem = self.dm_com.FindPicMem
        self.FindPicMemE = self.dm_com.FindPicMemE
        self.FindPicMemEx = self.dm_com.FindPicMemEx
        self.FindPicS = self.dm_com.FindPicS
        self.FindPicSim = self.dm_com.FindPicSim
        self.FindPicSimE = self.dm_com.FindPicSimE
        self.FindPicSimEx = self.dm_com.FindPicSimEx
        self.FindPicSimMem = self.dm_com.FindPicSimMem
        self.FindPicSimMemE = self.dm_com.FindPicSimMemE
        self.FindPicSimMemEx = self.dm_com.FindPicSimMemEx
        self.FindShape = self.dm_com.FindShape
        self.FindShapeE = self.dm_com.FindShapeE
        self.FindShapeEx = self.dm_com.FindShapeEx
        self.FindStr = self.dm_com.FindStr
        self.FindStrE = self.dm_com.FindStrE
        self.FindStrEx = self.dm_com.FindStrEx
        self.FindStrExS = self.dm_com.FindStrExS
        self.FindStrFast = self.dm_com.FindStrFast
        self.FindStrFastE = self.dm_com.FindStrFastE
        self.FindStrFastEx = self.dm_com.FindStrFastEx
        self.FindStrFastExS = self.dm_com.FindStrFastExS
        self.FindStrFastS = self.dm_com.FindStrFastS
        self.FindStrS = self.dm_com.FindStrS
        self.FindStrWithFont = self.dm_com.FindStrWithFont
        self.FindStrWithFontE = self.dm_com.FindStrWithFontE
        self.FindStrWithFontEx = self.dm_com.FindStrWithFontEx
        self.FindString = self.dm_com.FindString
        self.FindStringEx = self.dm_com.FindStringEx
        self.FindWindow = self.dm_com.FindWindow
        self.FindWindowByProcess = self.dm_com.FindWindowByProcess
        self.FindWindowByProcessId = self.dm_com.FindWindowByProcessId
        self.FindWindowEx = self.dm_com.FindWindowEx
        self.FindWindowSuper = self.dm_com.FindWindowSuper
        self.FloatToData = self.dm_com.FloatToData
        self.FoobarClearText = self.dm_com.FoobarClearText
        self.FoobarClose = self.dm_com.FoobarClose
        self.FoobarDrawLine = self.dm_com.FoobarDrawLine
        self.FoobarDrawPic = self.dm_com.FoobarDrawPic
        self.FoobarDrawText = self.dm_com.FoobarDrawText
        self.FoobarFillRect = self.dm_com.FoobarFillRect
        self.FoobarLock = self.dm_com.FoobarLock
        self.FoobarPrintText = self.dm_com.FoobarPrintText
        self.FoobarSetFont = self.dm_com.FoobarSetFont
        self.FoobarSetSave = self.dm_com.FoobarSetSave
        self.FoobarSetTrans = self.dm_com.FoobarSetTrans
        self.FoobarStartGif = self.dm_com.FoobarStartGif
        self.FoobarStopGif = self.dm_com.FoobarStopGif
        self.FoobarTextLineGap = self.dm_com.FoobarTextLineGap
        self.FoobarTextPrintDir = self.dm_com.FoobarTextPrintDir
        self.FoobarTextRect = self.dm_com.FoobarTextRect
        self.FoobarUnlock = self.dm_com.FoobarUnlock
        self.FoobarUpdate = self.dm_com.FoobarUpdate
        self.ForceUnBindWindow = self.dm_com.ForceUnBindWindow
        self.FreePic = self.dm_com.FreePic
        self.FreeProcessMemory = self.dm_com.FreeProcessMemory
        self.FreeScreenData = self.dm_com.FreeScreenData
        self.GetAveHSV = self.dm_com.GetAveHSV
        self.GetAveRGB = self.dm_com.GetAveRGB
        self.GetBasePath = self.dm_com.GetBasePath
        self.GetBindWindow = self.dm_com.GetBindWindow
        self.GetClientRect = self.dm_com.GetClientRect
        self.GetClientSize = self.dm_com.GetClientSize
        self.GetClipboard = self.dm_com.GetClipboard
        self.GetColor = self.dm_com.GetColor
        self.GetColorBGR = self.dm_com.GetColorBGR
        self.GetColorHSV = self.dm_com.GetColorHSV
        self.GetColorNum = self.dm_com.GetColorNum
        self.GetCommandLine = self.dm_com.GetCommandLine
        self.GetCpuType = self.dm_com.GetCpuType
        self.GetCpuUsage = self.dm_com.GetCpuUsage
        self.GetCursorPos = self.dm_com.GetCursorPos
        self.GetCursorShape = self.dm_com.GetCursorShape
        self.GetCursorShapeEx = self.dm_com.GetCursorShapeEx
        self.GetCursorSpot = self.dm_com.GetCursorSpot
        self.GetDPI = self.dm_com.GetDPI
        self.GetDict = self.dm_com.GetDict
        self.GetDictCount = self.dm_com.GetDictCount
        self.GetDictInfo = self.dm_com.GetDictInfo
        self.GetDir = self.dm_com.GetDir
        self.GetDiskModel = self.dm_com.GetDiskModel
        self.GetDiskReversion = self.dm_com.GetDiskReversion
        self.GetDiskSerial = self.dm_com.GetDiskSerial
        self.GetDisplayInfo = self.dm_com.GetDisplayInfo
        self.GetDmCount = self.dm_com.GetDmCount
        self.GetEnv = self.dm_com.GetEnv
        self.GetFileLength = self.dm_com.GetFileLength
        self.GetForegroundFocus = self.dm_com.GetForegroundFocus
        self.GetForegroundWindow = self.dm_com.GetForegroundWindow
        self.GetFps = self.dm_com.GetFps
        self.GetID = self.dm_com.GetID
        self.GetIDsOfNames = self.dm_com.GetIDsOfNames
        self.GetKeyState = self.dm_com.GetKeyState
        self.GetLastError = self.dm_com.GetLastError
        self.GetLocale = self.dm_com.GetLocale
        self.GetMac = self.dm_com.GetMac
        self.GetMachineCode = self.dm_com.GetMachineCode
        self.GetMachineCodeNoMac = self.dm_com.GetMachineCodeNoMac
        self.GetMemoryUsage = self.dm_com.GetMemoryUsage
        self.GetModuleBaseAddr = self.dm_com.GetModuleBaseAddr
        self.GetModuleSize = self.dm_com.GetModuleSize
        self.GetMousePointWindow = self.dm_com.GetMousePointWindow
        self.GetMouseSpeed = self.dm_com.GetMouseSpeed
        self.GetNetTime = self.dm_com.GetNetTime
        self.GetNetTimeByIp = self.dm_com.GetNetTimeByIp
        self.GetNetTimeSafe = self.dm_com.GetNetTimeSafe
        self.GetNowDict = self.dm_com.GetNowDict
        self.GetOsBuildNumber = self.dm_com.GetOsBuildNumber
        self.GetOsType = self.dm_com.GetOsType
        self.GetPath = self.dm_com.GetPath
        self.GetPicSize = self.dm_com.GetPicSize
        self.GetPointWindow = self.dm_com.GetPointWindow
        self.GetProcessInfo = self.dm_com.GetProcessInfo
        self.GetRealPath = self.dm_com.GetRealPath
        self.GetRemoteApiAddress = self.dm_com.GetRemoteApiAddress
        self.GetResultCount = self.dm_com.GetResultCount
        self.GetResultPos = self.dm_com.GetResultPos
        self.GetScreenData = self.dm_com.GetScreenData
        self.GetScreenDataBmp = self.dm_com.GetScreenDataBmp
        self.GetScreenDepth = self.dm_com.GetScreenDepth
        self.GetScreenHeight = self.dm_com.GetScreenHeight
        self.GetScreenWidth = self.dm_com.GetScreenWidth
        self.GetSpecialWindow = self.dm_com.GetSpecialWindow
        self.GetSystemInfo = self.dm_com.GetSystemInfo
        self.GetTime = self.dm_com.GetTime
        self.GetTypeInfo = self.dm_com.GetTypeInfo
        self.GetTypeInfoCount = self.dm_com.GetTypeInfoCount
        self.GetWindow = self.dm_com.GetWindow
        self.GetWindowClass = self.dm_com.GetWindowClass
        self.GetWindowProcessId = self.dm_com.GetWindowProcessId
        self.GetWindowProcessPath = self.dm_com.GetWindowProcessPath
        self.GetWindowRect = self.dm_com.GetWindowRect
        self.GetWindowState = self.dm_com.GetWindowState
        self.GetWindowThreadId = self.dm_com.GetWindowThreadId
        self.GetWindowTitle = self.dm_com.GetWindowTitle
        self.GetWordResultCount = self.dm_com.GetWordResultCount
        self.GetWordResultPos = self.dm_com.GetWordResultPos
        self.GetWordResultStr = self.dm_com.GetWordResultStr
        self.GetWords = self.dm_com.GetWords
        self.GetWordsNoDict = self.dm_com.GetWordsNoDict
        self.HackSpeed = self.dm_com.HackSpeed
        self.Hex32 = self.dm_com.Hex32
        self.Hex64 = self.dm_com.Hex64
        self.ImageToBmp = self.dm_com.ImageToBmp
        self.InitCri = self.dm_com.InitCri
        self.Int64ToInt32 = self.dm_com.Int64ToInt32
        self.IntToData = self.dm_com.IntToData
        self.Invoke = self.dm_com.Invoke
        self.Is64Bit = self.dm_com.Is64Bit
        self.IsBind = self.dm_com.IsBind
        self.IsDisplayDead = self.dm_com.IsDisplayDead
        self.IsFileExist = self.dm_com.IsFileExist
        self.IsFolderExist = self.dm_com.IsFolderExist
        self.IsSurrpotVt = self.dm_com.IsSurrpotVt
        self.KeyDown = self.dm_com.KeyDown
        self.KeyDownChar = self.dm_com.KeyDownChar
        self.KeyPress = self.dm_com.KeyPress
        self.KeyPressStr = self.dm_com.KeyPressStr
        self.KeyUp = self.dm_com.KeyUp
        self.KeyUpChar = self.dm_com.KeyUpChar
        self.LeaveCri = self.dm_com.LeaveCri
        self.LeftClick = self.dm_com.LeftClick
        self.LeftDoubleClick = self.dm_com.LeftDoubleClick
        self.LeftDown = self.dm_com.LeftDown
        self.LeftUp = self.dm_com.LeftUp
        self.LoadAi = self.dm_com.LoadAi
        self.LoadAiMemory = self.dm_com.LoadAiMemory
        self.LoadPic = self.dm_com.LoadPic
        self.LoadPicByte = self.dm_com.LoadPicByte
        self.LockDisplay = self.dm_com.LockDisplay
        self.LockInput = self.dm_com.LockInput
        self.LockMouseRect = self.dm_com.LockMouseRect
        self.Log = self.dm_com.Log
        self.MatchPicName = self.dm_com.MatchPicName
        self.Md5 = self.dm_com.Md5
        self.MiddleClick = self.dm_com.MiddleClick
        self.MiddleDown = self.dm_com.MiddleDown
        self.MiddleUp = self.dm_com.MiddleUp
        self.MoveDD = self.dm_com.MoveDD
        self.MoveFile = self.dm_com.MoveFile
        self.MoveR = self.dm_com.MoveR
        self.MoveTo = self.dm_com.MoveTo
        self.MoveToEx = self.dm_com.MoveToEx
        self.MoveWindow = self.dm_com.MoveWindow
        self.Ocr = self.dm_com.Ocr
        self.OcrEx = self.dm_com.OcrEx
        self.OcrExOne = self.dm_com.OcrExOne
        self.OcrInFile = self.dm_com.OcrInFile
        self.OpenProcess = self.dm_com.OpenProcess
        self.Play = self.dm_com.Play
        self.QueryInterface = self.dm_com.QueryInterface
        self.RGB2BGR = self.dm_com.RGB2BGR
        self.ReadData = self.dm_com.ReadData
        self.ReadDataAddr = self.dm_com.ReadDataAddr
        self.ReadDataAddrToBin = self.dm_com.ReadDataAddrToBin
        self.ReadDataToBin = self.dm_com.ReadDataToBin
        self.ReadDouble = self.dm_com.ReadDouble
        self.ReadDoubleAddr = self.dm_com.ReadDoubleAddr
        self.ReadFile = self.dm_com.ReadFile
        self.ReadFileData = self.dm_com.ReadFileData
        self.ReadFloat = self.dm_com.ReadFloat
        self.ReadFloatAddr = self.dm_com.ReadFloatAddr
        self.ReadIni = self.dm_com.ReadIni
        self.ReadIniPwd = self.dm_com.ReadIniPwd
        self.ReadInt = self.dm_com.ReadInt
        self.ReadIntAddr = self.dm_com.ReadIntAddr
        self.ReadString = self.dm_com.ReadString
        self.ReadStringAddr = self.dm_com.ReadStringAddr
        self.Reg = self.dm_com.Reg
        self.RegEx = self.dm_com.RegEx
        self.RegExNoMac = self.dm_com.RegExNoMac
        self.RegNoMac = self.dm_com.RegNoMac
        self.Release = self.dm_com.Release
        self.ReleaseRef = self.dm_com.ReleaseRef
        self.RightClick = self.dm_com.RightClick
        self.RightDown = self.dm_com.RightDown
        self.RightUp = self.dm_com.RightUp
        self.RunApp = self.dm_com.RunApp
        self.SaveDict = self.dm_com.SaveDict
        self.ScreenToClient = self.dm_com.ScreenToClient
        self.SelectDirectory = self.dm_com.SelectDirectory
        self.SelectFile = self.dm_com.SelectFile
        self.SendCommand = self.dm_com.SendCommand
        self.SendPaste = self.dm_com.SendPaste
        self.SendString = self.dm_com.SendString
        self.SendString2 = self.dm_com.SendString2
        self.SendStringIme = self.dm_com.SendStringIme
        self.SendStringIme2 = self.dm_com.SendStringIme2
        self.SetAero = self.dm_com.SetAero
        self.SetAsmHwndAsProcessId = self.dm_com.SetAsmHwndAsProcessId
        self.SetClientSize = self.dm_com.SetClientSize
        self.SetClipboard = self.dm_com.SetClipboard
        self.SetColGapNoDict = self.dm_com.SetColGapNoDict
        self.SetDict = self.dm_com.SetDict
        self.SetDictMem = self.dm_com.SetDictMem
        self.SetDictPwd = self.dm_com.SetDictPwd
        self.SetDisplayAcceler = self.dm_com.SetDisplayAcceler
        self.SetDisplayDelay = self.dm_com.SetDisplayDelay
        self.SetDisplayInput = self.dm_com.SetDisplayInput
        self.SetDisplayRefreshDelay = self.dm_com.SetDisplayRefreshDelay
        self.SetEnumWindowDelay = self.dm_com.SetEnumWindowDelay
        self.SetEnv = self.dm_com.SetEnv
        self.SetExactOcr = self.dm_com.SetExactOcr
        self.SetExcludeRegion = self.dm_com.SetExcludeRegion
        self.SetExitThread = self.dm_com.SetExitThread
        self.SetExportDict = self.dm_com.SetExportDict
        self.SetFindPicMultithreadCount = self.dm_com.SetFindPicMultithreadCount
        self.SetFindPicMultithreadLimit = self.dm_com.SetFindPicMultithreadLimit
        self.SetInputDm = self.dm_com.SetInputDm
        self.SetKeypadDelay = self.dm_com.SetKeypadDelay
        self.SetLocale = self.dm_com.SetLocale
        self.SetMemoryFindResultToFile = self.dm_com.SetMemoryFindResultToFile
        self.SetMemoryHwndAsProcessId = self.dm_com.SetMemoryHwndAsProcessId
        self.SetMinColGap = self.dm_com.SetMinColGap
        self.SetMinRowGap = self.dm_com.SetMinRowGap
        self.SetMouseDelay = self.dm_com.SetMouseDelay
        self.SetMouseSpeed = self.dm_com.SetMouseSpeed
        self.SetParam64ToPointer = self.dm_com.SetParam64ToPointer
        self.SetPath = self.dm_com.SetPath
        self.SetPicPwd = self.dm_com.SetPicPwd
        self.SetRowGapNoDict = self.dm_com.SetRowGapNoDict
        self.SetScreen = self.dm_com.SetScreen
        self.SetSendStringDelay = self.dm_com.SetSendStringDelay
        self.SetShowAsmErrorMsg = self.dm_com.SetShowAsmErrorMsg
        self.SetShowErrorMsg = self.dm_com.SetShowErrorMsg
        self.SetSimMode = self.dm_com.SetSimMode
        self.SetUAC = self.dm_com.SetUAC
        self.SetWindowSize = self.dm_com.SetWindowSize
        self.SetWindowState = self.dm_com.SetWindowState
        self.SetWindowText = self.dm_com.SetWindowText
        self.SetWindowTransparent = self.dm_com.SetWindowTransparent
        self.SetWordGap = self.dm_com.SetWordGap
        self.SetWordGapNoDict = self.dm_com.SetWordGapNoDict
        self.SetWordLineHeight = self.dm_com.SetWordLineHeight
        self.SetWordLineHeightNoDict = self.dm_com.SetWordLineHeightNoDict
        self.ShowScrMsg = self.dm_com.ShowScrMsg
        self.ShowTaskBarIcon = self.dm_com.ShowTaskBarIcon
        self.SortPosDistance = self.dm_com.SortPosDistance
        self.SpeedNormalGraphic = self.dm_com.SpeedNormalGraphic
        self.Stop = self.dm_com.Stop
        self.StrStr = self.dm_com.StrStr
        self.StringToData = self.dm_com.StringToData
        self.SwitchBindWindow = self.dm_com.SwitchBindWindow
        self.TerminateProcess = self.dm_com.TerminateProcess
        self.TerminateProcessTree = self.dm_com.TerminateProcessTree
        self.UnBindWindow = self.dm_com.UnBindWindow
        self.UnLoadDriver = self.dm_com.UnLoadDriver
        self.UseDict = self.dm_com.UseDict
        self.Ver = self.dm_com.Ver
        self.VirtualAllocEx = self.dm_com.VirtualAllocEx
        self.VirtualFreeEx = self.dm_com.VirtualFreeEx
        self.VirtualProtectEx = self.dm_com.VirtualProtectEx
        self.VirtualQueryEx = self.dm_com.VirtualQueryEx
        self.WaitKey = self.dm_com.WaitKey
        self.WheelDown = self.dm_com.WheelDown
        self.WheelUp = self.dm_com.WheelUp
        self.WriteData = self.dm_com.WriteData
        self.WriteDataAddr = self.dm_com.WriteDataAddr
        self.WriteDataAddrFromBin = self.dm_com.WriteDataAddrFromBin
        self.WriteDataFromBin = self.dm_com.WriteDataFromBin
        self.WriteDouble = self.dm_com.WriteDouble
        self.WriteDoubleAddr = self.dm_com.WriteDoubleAddr
        self.WriteFile = self.dm_com.WriteFile
        self.WriteFloat = self.dm_com.WriteFloat
        self.WriteFloatAddr = self.dm_com.WriteFloatAddr
        self.WriteIni = self.dm_com.WriteIni
        self.WriteIniPwd = self.dm_com.WriteIniPwd
        self.WriteInt = self.dm_com.WriteInt
        self.WriteIntAddr = self.dm_com.WriteIntAddr
        self.WriteString = self.dm_com.WriteString
        self.WriteStringAddr = self.dm_com.WriteStringAddr
        self.delay = self.dm_com.delay

    def get_all_from_dm_com_3_1233(self):
        """ 加载 3.1233版本的 全部公开方法"""
        self.ActiveInputMethod = self.dm_com.ActiveInputMethod
        self.AddDict = self.dm_com.AddDict
        self.AddRef = self.dm_com.AddRef
        self.AppendPicAddr = self.dm_com.AppendPicAddr
        self.AsmAdd = self.dm_com.AsmAdd
        self.AsmCall = self.dm_com.AsmCall
        self.AsmClear = self.dm_com.AsmClear
        self.AsmCode = self.dm_com.AsmCode
        self.Assemble = self.dm_com.Assemble
        self.BGR2RGB = self.dm_com.BGR2RGB
        self.Beep = self.dm_com.Beep
        self.BindWindow = self.dm_com.BindWindow
        self.BindWindowEx = self.dm_com.BindWindowEx
        self.Capture = self.dm_com.Capture
        self.CaptureGif = self.dm_com.CaptureGif
        self.CaptureJpg = self.dm_com.CaptureJpg
        self.CapturePng = self.dm_com.CapturePng
        self.CapturePre = self.dm_com.CapturePre
        self.CheckFontSmooth = self.dm_com.CheckFontSmooth
        self.CheckInputMethod = self.dm_com.CheckInputMethod
        self.CheckUAC = self.dm_com.CheckUAC
        self.ClearDict = self.dm_com.ClearDict
        self.ClientToScreen = self.dm_com.ClientToScreen
        self.CmpColor = self.dm_com.CmpColor
        self.CopyFile = self.dm_com.CopyFile
        self.CreateFolder = self.dm_com.CreateFolder
        self.CreateFoobarCustom = self.dm_com.CreateFoobarCustom
        self.CreateFoobarEllipse = self.dm_com.CreateFoobarEllipse
        self.CreateFoobarRect = self.dm_com.CreateFoobarRect
        self.CreateFoobarRoundRect = self.dm_com.CreateFoobarRoundRect
        self.DecodeFile = self.dm_com.DecodeFile
        self.DelEnv = self.dm_com.DelEnv
        self.DeleteFile = self.dm_com.DeleteFile
        self.DeleteFolder = self.dm_com.DeleteFolder
        self.DeleteIni = self.dm_com.DeleteIni
        self.DeleteIniPwd = self.dm_com.DeleteIniPwd
        self.DisableFontSmooth = self.dm_com.DisableFontSmooth
        self.DisablePowerSave = self.dm_com.DisablePowerSave
        self.DisableScreenSave = self.dm_com.DisableScreenSave
        self.DmGuard = self.dm_com.DmGuard
        self.DoubleToData = self.dm_com.DoubleToData
        self.DownCpu = self.dm_com.DownCpu
        self.DownloadFile = self.dm_com.DownloadFile
        self.EnableBind = self.dm_com.EnableBind
        self.EnableDisplayDebug = self.dm_com.EnableDisplayDebug
        self.EnableFakeActive = self.dm_com.EnableFakeActive
        self.EnableGetColorByCapture = self.dm_com.EnableGetColorByCapture
        self.EnableIme = self.dm_com.EnableIme
        self.EnableKeypadMsg = self.dm_com.EnableKeypadMsg
        self.EnableKeypadPatch = self.dm_com.EnableKeypadPatch
        self.EnableKeypadSync = self.dm_com.EnableKeypadSync
        self.EnableMouseMsg = self.dm_com.EnableMouseMsg
        self.EnableMouseSync = self.dm_com.EnableMouseSync
        self.EnableRealKeypad = self.dm_com.EnableRealKeypad
        self.EnableRealMouse = self.dm_com.EnableRealMouse
        self.EnableSpeedDx = self.dm_com.EnableSpeedDx
        self.EncodeFile = self.dm_com.EncodeFile
        self.EnterCri = self.dm_com.EnterCri
        self.EnumWindow = self.dm_com.EnumWindow
        self.EnumWindowByProcess = self.dm_com.EnumWindowByProcess
        self.EnumWindowSuper = self.dm_com.EnumWindowSuper
        self.ExcludePos = self.dm_com.ExcludePos
        self.ExitOs = self.dm_com.ExitOs
        self.FaqCancel = self.dm_com.FaqCancel
        self.FaqCapture = self.dm_com.FaqCapture
        self.FaqCaptureFromFile = self.dm_com.FaqCaptureFromFile
        self.FaqFetch = self.dm_com.FaqFetch
        self.FaqGetSize = self.dm_com.FaqGetSize
        self.FaqPost = self.dm_com.FaqPost
        self.FaqRelease = self.dm_com.FaqRelease
        self.FaqSend = self.dm_com.FaqSend
        self.FetchWord = self.dm_com.FetchWord
        self.FindColor = self.dm_com.FindColor
        self.FindColorE = self.dm_com.FindColorE
        self.FindColorEx = self.dm_com.FindColorEx
        self.FindData = self.dm_com.FindData
        self.FindDataEx = self.dm_com.FindDataEx
        self.FindDouble = self.dm_com.FindDouble
        self.FindDoubleEx = self.dm_com.FindDoubleEx
        self.FindFloat = self.dm_com.FindFloat
        self.FindFloatEx = self.dm_com.FindFloatEx
        self.FindInputMethod = self.dm_com.FindInputMethod
        self.FindInt = self.dm_com.FindInt
        self.FindIntEx = self.dm_com.FindIntEx
        self.FindMulColor = self.dm_com.FindMulColor
        self.FindMultiColor = self.dm_com.FindMultiColor
        self.FindMultiColorE = self.dm_com.FindMultiColorE
        self.FindMultiColorEx = self.dm_com.FindMultiColorEx
        self.FindNearestPos = self.dm_com.FindNearestPos
        self.FindPic = self.dm_com.FindPic
        self.FindPicE = self.dm_com.FindPicE
        self.FindPicEx = self.dm_com.FindPicEx
        self.FindPicExS = self.dm_com.FindPicExS
        self.FindPicMem = self.dm_com.FindPicMem
        self.FindPicMemE = self.dm_com.FindPicMemE
        self.FindPicMemEx = self.dm_com.FindPicMemEx
        self.FindPicS = self.dm_com.FindPicS
        self.FindShape = self.dm_com.FindShape
        self.FindShapeE = self.dm_com.FindShapeE
        self.FindShapeEx = self.dm_com.FindShapeEx
        self.FindStr = self.dm_com.FindStr
        self.FindStrE = self.dm_com.FindStrE
        self.FindStrEx = self.dm_com.FindStrEx
        self.FindStrExS = self.dm_com.FindStrExS
        self.FindStrFast = self.dm_com.FindStrFast
        self.FindStrFastE = self.dm_com.FindStrFastE
        self.FindStrFastEx = self.dm_com.FindStrFastEx
        self.FindStrFastExS = self.dm_com.FindStrFastExS
        self.FindStrFastS = self.dm_com.FindStrFastS
        self.FindStrS = self.dm_com.FindStrS
        self.FindStrWithFont = self.dm_com.FindStrWithFont
        self.FindStrWithFontE = self.dm_com.FindStrWithFontE
        self.FindStrWithFontEx = self.dm_com.FindStrWithFontEx
        self.FindString = self.dm_com.FindString
        self.FindStringEx = self.dm_com.FindStringEx
        self.FindWindow = self.dm_com.FindWindow
        self.FindWindowByProcess = self.dm_com.FindWindowByProcess
        self.FindWindowByProcessId = self.dm_com.FindWindowByProcessId
        self.FindWindowEx = self.dm_com.FindWindowEx
        self.FindWindowSuper = self.dm_com.FindWindowSuper
        self.FloatToData = self.dm_com.FloatToData
        self.FoobarClearText = self.dm_com.FoobarClearText
        self.FoobarClose = self.dm_com.FoobarClose
        self.FoobarDrawLine = self.dm_com.FoobarDrawLine
        self.FoobarDrawPic = self.dm_com.FoobarDrawPic
        self.FoobarDrawText = self.dm_com.FoobarDrawText
        self.FoobarFillRect = self.dm_com.FoobarFillRect
        self.FoobarLock = self.dm_com.FoobarLock
        self.FoobarPrintText = self.dm_com.FoobarPrintText
        self.FoobarSetFont = self.dm_com.FoobarSetFont
        self.FoobarSetSave = self.dm_com.FoobarSetSave
        self.FoobarTextLineGap = self.dm_com.FoobarTextLineGap
        self.FoobarTextPrintDir = self.dm_com.FoobarTextPrintDir
        self.FoobarTextRect = self.dm_com.FoobarTextRect
        self.FoobarUnlock = self.dm_com.FoobarUnlock
        self.FoobarUpdate = self.dm_com.FoobarUpdate
        self.ForceUnBindWindow = self.dm_com.ForceUnBindWindow
        self.FreePic = self.dm_com.FreePic
        self.FreeScreenData = self.dm_com.FreeScreenData
        self.GetAveHSV = self.dm_com.GetAveHSV
        self.GetAveRGB = self.dm_com.GetAveRGB
        self.GetBasePath = self.dm_com.GetBasePath
        self.GetClientRect = self.dm_com.GetClientRect
        self.GetClientSize = self.dm_com.GetClientSize
        self.GetClipboard = self.dm_com.GetClipboard
        self.GetColor = self.dm_com.GetColor
        self.GetColorBGR = self.dm_com.GetColorBGR
        self.GetColorHSV = self.dm_com.GetColorHSV
        self.GetColorNum = self.dm_com.GetColorNum
        self.GetCursorPos = self.dm_com.GetCursorPos
        self.GetCursorShape = self.dm_com.GetCursorShape
        self.GetCursorShapeEx = self.dm_com.GetCursorShapeEx
        self.GetCursorSpot = self.dm_com.GetCursorSpot
        self.GetDict = self.dm_com.GetDict
        self.GetDictCount = self.dm_com.GetDictCount
        self.GetDictInfo = self.dm_com.GetDictInfo
        self.GetDir = self.dm_com.GetDir
        self.GetDiskSerial = self.dm_com.GetDiskSerial
        self.GetDmCount = self.dm_com.GetDmCount
        self.GetEnv = self.dm_com.GetEnv
        self.GetFileLength = self.dm_com.GetFileLength
        self.GetForegroundFocus = self.dm_com.GetForegroundFocus
        self.GetForegroundWindow = self.dm_com.GetForegroundWindow
        self.GetID = self.dm_com.GetID
        self.GetIDsOfNames = self.dm_com.GetIDsOfNames
        self.GetKeyState = self.dm_com.GetKeyState
        self.GetLastError = self.dm_com.GetLastError
        self.GetMac = self.dm_com.GetMac
        self.GetMachineCode = self.dm_com.GetMachineCode
        self.GetMachineCodeNoMac = self.dm_com.GetMachineCodeNoMac
        self.GetModuleBaseAddr = self.dm_com.GetModuleBaseAddr
        self.GetMousePointWindow = self.dm_com.GetMousePointWindow
        self.GetNetTime = self.dm_com.GetNetTime
        self.GetNetTimeSafe = self.dm_com.GetNetTimeSafe
        self.GetNowDict = self.dm_com.GetNowDict
        self.GetOsType = self.dm_com.GetOsType
        self.GetPath = self.dm_com.GetPath
        self.GetPicSize = self.dm_com.GetPicSize
        self.GetPointWindow = self.dm_com.GetPointWindow
        self.GetResultCount = self.dm_com.GetResultCount
        self.GetResultPos = self.dm_com.GetResultPos
        self.GetScreenData = self.dm_com.GetScreenData
        self.GetScreenDataBmp = self.dm_com.GetScreenDataBmp
        self.GetScreenDepth = self.dm_com.GetScreenDepth
        self.GetScreenHeight = self.dm_com.GetScreenHeight
        self.GetScreenWidth = self.dm_com.GetScreenWidth
        self.GetSpecialWindow = self.dm_com.GetSpecialWindow
        self.GetTime = self.dm_com.GetTime
        self.GetTypeInfo = self.dm_com.GetTypeInfo
        self.GetTypeInfoCount = self.dm_com.GetTypeInfoCount
        self.GetWindow = self.dm_com.GetWindow
        self.GetWindowClass = self.dm_com.GetWindowClass
        self.GetWindowProcessId = self.dm_com.GetWindowProcessId
        self.GetWindowProcessPath = self.dm_com.GetWindowProcessPath
        self.GetWindowRect = self.dm_com.GetWindowRect
        self.GetWindowState = self.dm_com.GetWindowState
        self.GetWindowTitle = self.dm_com.GetWindowTitle
        self.GetWordResultCount = self.dm_com.GetWordResultCount
        self.GetWordResultPos = self.dm_com.GetWordResultPos
        self.GetWordResultStr = self.dm_com.GetWordResultStr
        self.GetWords = self.dm_com.GetWords
        self.GetWordsNoDict = self.dm_com.GetWordsNoDict
        self.ImageToBmp = self.dm_com.ImageToBmp
        self.IntToData = self.dm_com.IntToData
        self.Invoke = self.dm_com.Invoke
        self.Is64Bit = self.dm_com.Is64Bit
        self.IsBind = self.dm_com.IsBind
        self.IsDisplayDead = self.dm_com.IsDisplayDead
        self.IsFileExist = self.dm_com.IsFileExist
        self.KeyDown = self.dm_com.KeyDown
        self.KeyDownChar = self.dm_com.KeyDownChar
        self.KeyPress = self.dm_com.KeyPress
        self.KeyPressChar = self.dm_com.KeyPressChar
        self.KeyPressStr = self.dm_com.KeyPressStr
        self.KeyUp = self.dm_com.KeyUp
        self.KeyUpChar = self.dm_com.KeyUpChar
        self.LeaveCri = self.dm_com.LeaveCri
        self.LeftClick = self.dm_com.LeftClick
        self.LeftDoubleClick = self.dm_com.LeftDoubleClick
        self.LeftDown = self.dm_com.LeftDown
        self.LeftUp = self.dm_com.LeftUp
        self.LoadPic = self.dm_com.LoadPic
        self.LockDisplay = self.dm_com.LockDisplay
        self.LockInput = self.dm_com.LockInput
        self.LockMouseRect = self.dm_com.LockMouseRect
        self.Log = self.dm_com.Log
        self.MatchPicName = self.dm_com.MatchPicName
        self.Md5 = self.dm_com.Md5
        self.MiddleClick = self.dm_com.MiddleClick
        self.MoveDD = self.dm_com.MoveDD
        self.MoveFile = self.dm_com.MoveFile
        self.MoveR = self.dm_com.MoveR
        self.MoveTo = self.dm_com.MoveTo
        self.MoveToEx = self.dm_com.MoveToEx
        self.MoveWindow = self.dm_com.MoveWindow
        self.Ocr = self.dm_com.Ocr
        self.OcrEx = self.dm_com.OcrEx
        self.OcrInFile = self.dm_com.OcrInFile
        self.Play = self.dm_com.Play
        self.QueryInterface = self.dm_com.QueryInterface
        self.RGB2BGR = self.dm_com.RGB2BGR
        self.ReadData = self.dm_com.ReadData
        self.ReadDouble = self.dm_com.ReadDouble
        self.ReadFile = self.dm_com.ReadFile
        self.ReadFloat = self.dm_com.ReadFloat
        self.ReadIni = self.dm_com.ReadIni
        self.ReadIniPwd = self.dm_com.ReadIniPwd
        self.ReadInt = self.dm_com.ReadInt
        self.ReadString = self.dm_com.ReadString
        self.Reg = self.dm_com.Reg
        self.RegEx = self.dm_com.RegEx
        self.RegExNoMac = self.dm_com.RegExNoMac
        self.RegNoMac = self.dm_com.RegNoMac
        self.Release = self.dm_com.Release
        self.RightClick = self.dm_com.RightClick
        self.RightDown = self.dm_com.RightDown
        self.RightUp = self.dm_com.RightUp
        self.RunApp = self.dm_com.RunApp
        self.SaveDict = self.dm_com.SaveDict
        self.ScreenToClient = self.dm_com.ScreenToClient
        self.SelectDirectory = self.dm_com.SelectDirectory
        self.SelectFile = self.dm_com.SelectFile
        self.SendCommand = self.dm_com.SendCommand
        self.SendPaste = self.dm_com.SendPaste
        self.SendString = self.dm_com.SendString
        self.SendString2 = self.dm_com.SendString2
        self.SendStringIme = self.dm_com.SendStringIme
        self.SetClientSize = self.dm_com.SetClientSize
        self.SetClipboard = self.dm_com.SetClipboard
        self.SetColGapNoDict = self.dm_com.SetColGapNoDict
        self.SetDict = self.dm_com.SetDict
        self.SetDictMem = self.dm_com.SetDictMem
        self.SetDictPwd = self.dm_com.SetDictPwd
        self.SetDisplayAcceler = self.dm_com.SetDisplayAcceler
        self.SetDisplayDelay = self.dm_com.SetDisplayDelay
        self.SetDisplayInput = self.dm_com.SetDisplayInput
        self.SetEnumWindowDelay = self.dm_com.SetEnumWindowDelay
        self.SetEnv = self.dm_com.SetEnv
        self.SetExactOcr = self.dm_com.SetExactOcr
        self.SetExportDict = self.dm_com.SetExportDict
        self.SetKeypadDelay = self.dm_com.SetKeypadDelay
        self.SetMemoryFindResultToFile = self.dm_com.SetMemoryFindResultToFile
        self.SetMemoryHwndAsProcessId = self.dm_com.SetMemoryHwndAsProcessId
        self.SetMinColGap = self.dm_com.SetMinColGap
        self.SetMinRowGap = self.dm_com.SetMinRowGap
        self.SetMouseDelay = self.dm_com.SetMouseDelay
        self.SetPath = self.dm_com.SetPath
        self.SetPicPwd = self.dm_com.SetPicPwd
        self.SetRowGapNoDict = self.dm_com.SetRowGapNoDict
        self.SetScreen = self.dm_com.SetScreen
        self.SetShowErrorMsg = self.dm_com.SetShowErrorMsg
        self.SetSimMode = self.dm_com.SetSimMode
        self.SetUAC = self.dm_com.SetUAC
        self.SetWindowSize = self.dm_com.SetWindowSize
        self.SetWindowState = self.dm_com.SetWindowState
        self.SetWindowText = self.dm_com.SetWindowText
        self.SetWindowTransparent = self.dm_com.SetWindowTransparent
        self.SetWordGap = self.dm_com.SetWordGap
        self.SetWordGapNoDict = self.dm_com.SetWordGapNoDict
        self.SetWordLineHeight = self.dm_com.SetWordLineHeight
        self.SetWordLineHeightNoDict = self.dm_com.SetWordLineHeightNoDict
        self.ShowScrMsg = self.dm_com.ShowScrMsg
        self.SortPosDistance = self.dm_com.SortPosDistance
        self.Stop = self.dm_com.Stop
        self.StrStr = self.dm_com.StrStr
        self.StringToData = self.dm_com.StringToData
        self.UnBindWindow = self.dm_com.UnBindWindow
        self.UseDict = self.dm_com.UseDict
        self.Ver = self.dm_com.Ver
        self.WaitKey = self.dm_com.WaitKey
        self.WheelDown = self.dm_com.WheelDown
        self.WheelUp = self.dm_com.WheelUp
        self.WriteData = self.dm_com.WriteData
        self.WriteDouble = self.dm_com.WriteDouble
        self.WriteFile = self.dm_com.WriteFile
        self.WriteFloat = self.dm_com.WriteFloat
        self.WriteIni = self.dm_com.WriteIni
        self.WriteIniPwd = self.dm_com.WriteIniPwd
        self.WriteInt = self.dm_com.WriteInt
        self.WriteString = self.dm_com.WriteString
        self.delay = self.dm_com.delay


if __name__ == '__main__':
    # dm = Dm(reg_code_append_key="jk0178633330", reg_code="lumiku2fdc744d96597f65888674a63fb3489a")
    # """注册码：lumiku2fdc744d96597f65888674a63fb3489a附加码： yk3553771677"""

    dm = Dm(version = 7, reg_code_append_key="jk0178633330", reg_code="lumiku2fdc744d96597f65888674a63fb3489a")
    while 1:
        print('循环中')
        time.sleep(1)

