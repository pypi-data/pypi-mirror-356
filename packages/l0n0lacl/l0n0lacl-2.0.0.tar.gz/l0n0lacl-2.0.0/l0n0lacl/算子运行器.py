from .张量 import 张量, 张量列表
from .数组 import 数组
from .标量 import 标量, 标量数组
from .设备内存 import 设备内存
from .动态库加载器 import 加载库
from .日志 import 记录错误日志并抛出异常, 记录acl返回值错误日志并抛出异常
from typing import Dict, Tuple
import numpy as np
import os
import ctypes
import re


ascend_home_path = os.environ["ASCEND_HOME_PATH"]
ascend_opp_path = os.environ['ASCEND_OPP_PATH']
不使用自定义算子 = os.environ.get('NO_VENDORS_OPP') == '1'

_自定义算子缓存 = {}
_官方算子缓存 = {}


def _缓存算子(库内容: str, 库目录: str, 自定义: bool):
    算子名称迭代器 = re.finditer(r'aclnn(.+)GetWorkspaceSize', 库内容)
    for 算子名称匹配结果 in 算子名称迭代器:
        算子名称 = 算子名称匹配结果.group(1)
        if 自定义:
            _自定义算子缓存[算子名称] = 加载库(库目录)
        else:
            _官方算子缓存[算子名称] = 加载库(库目录)


def 缓存所有算子库():
    # 自定义库
    前缀目录 = f'{ascend_opp_path}/vendors'
    for 算子前缀 in os.listdir(前缀目录):
        算子前缀目录 = f'{前缀目录}/{算子前缀}'
        if not os.path.isdir(算子前缀目录):
            continue
        库目录 = f'{算子前缀目录}/op_api/lib/libcust_opapi.so'
        结果 = os.popen(
            f'nm -D {库目录} | grep -e "GetWorkspaceSize"').read().strip()
        if len(结果) < 0:
            continue
        _缓存算子(结果, 库目录, True)

    nn算子目录 = f"{ascend_home_path}/lib64/libopapi.so"
    结果 = os.popen(
        f'nm -D {nn算子目录} | grep -e "GetWorkspaceSize"').read().strip()
    _缓存算子(结果, nn算子目录, False)


缓存所有算子库()

_找到的自定义算子缓存: Dict[str, Tuple] = {}
_找到的官方算子缓存: Dict[str, Tuple] = {}


def 寻找算子Api(算子名称: str):
    if 不使用自定义算子:
        缓存 = _找到的官方算子缓存.get(算子名称)
    else:
        缓存 = _找到的自定义算子缓存.get(算子名称) or _找到的官方算子缓存.get(算子名称)
    if 缓存 is not None:
        return 缓存

    自定义算子中找到的 = False
    if 不使用自定义算子:
        库 = _官方算子缓存.get(算子名称)
    else:
        库 = _自定义算子缓存.get(算子名称)
        if 库 is not None:
            自定义算子中找到的 = True
        库 = _官方算子缓存.get(算子名称)
    if 库 is None:
        记录错误日志并抛出异常(f"算子[{算子名称}]没找到对应的库")
    GetWorkspace: ctypes._FuncPointer = getattr(
        库, f"aclnn{算子名称}GetWorkspaceSize")
    算子运行Api: ctypes._FuncPointer = getattr(库, f"aclnn{算子名称}")
    if GetWorkspace is None:
        raise Exception(f"aclnn{算子名称}GetWorkspaceSize 没找到")
    if 算子运行Api is None:
        raise Exception(f"aclnn{算子名称} 没找到")
    GetWorkspace.restype = ctypes.c_int
    算子运行Api.argtypes = [
        ctypes.c_void_p,  # workspace指针
        ctypes.c_uint64,  # workspace大小
        ctypes.c_void_p,  # 运行器(executor)
        ctypes.c_void_p,  # 流水线(stream)
    ]
    算子运行Api.restype = ctypes.c_int

    if 自定义算子中找到的:
        _找到的自定义算子缓存[算子名称] = (GetWorkspace, 算子运行Api)
    else:
        _找到的官方算子缓存[算子名称] = (GetWorkspace, 算子运行Api)

    return GetWorkspace, 算子运行Api


class 算子运行器:
    def __init__(self, 算子名称) -> None:
        self.获取workspace大小函数, self.算子执行函数 = 寻找算子Api(算子名称)
        self.executor = np.array([0], dtype=np.uint64)
        self.参数保持不被销毁缓存: list
        self.workspace内存 = None

    def 检测将要运行的设备索引(self, *args):
        设备索引 = None
        for arg in args:
            if ((not isinstance(arg, 张量))
                and (not isinstance(arg, 张量列表))
                and (not isinstance(arg, 标量))
                and (not isinstance(arg, 标量数组))
                    and (not isinstance(arg, 数组))):
                continue
            if 设备索引 is None:
                设备索引 = arg.设备索引
            elif 设备索引 != arg.设备索引:
                raise Exception('参数应该在同一个设备上')
        return 设备索引

    def 根据输入将ndarray创建为张量并缓存参数(self, *args):
        设备索引 = self.检测将要运行的设备索引(*args)
        self.参数保持不被销毁缓存 = []
        for arg in args:
            if isinstance(arg, np.ndarray):
                self.参数保持不被销毁缓存.append(张量(arg, 设备索引=设备索引))
            elif isinstance(arg, list):
                if isinstance(arg[0], np.ndarray) or isinstance(arg[0], 张量):
                    self.参数保持不被销毁缓存.append(张量列表(arg, 设备索引=设备索引))
                else:
                    self.参数保持不被销毁缓存.append(数组(arg, 设备索引=设备索引))
            else:
                self.参数保持不被销毁缓存.append(arg)

    def GetWorkspaceSize函数的参数(self):
        调用算子时传入的参数 = []
        for arg in self.参数保持不被销毁缓存:
            if (isinstance(arg, 张量)
                or isinstance(arg, 张量列表)
                or isinstance(arg, 标量)
                or isinstance(arg, 标量数组)
                    or isinstance(arg, 数组)):
                调用算子时传入的参数.append(arg.指针)
            elif (isinstance(arg, ctypes.c_int8)
                  or isinstance(arg, ctypes.c_int16)
                  or isinstance(arg, ctypes.c_int32)
                  or isinstance(arg, ctypes.c_int64)
                  or isinstance(arg, ctypes.c_float)
                  or isinstance(arg, ctypes.c_double)
                  or isinstance(arg, ctypes.c_uint8)
                  or isinstance(arg, ctypes.c_uint16)
                  or isinstance(arg, ctypes.c_uint32)
                  or isinstance(arg, ctypes.c_uint64)):
                调用算子时传入的参数.append(arg.value)
            else:
                调用算子时传入的参数.append(arg)
        workspace = np.zeros([1], dtype=np.uint64)
        调用算子时传入的参数.append(workspace.ctypes.data)
        调用算子时传入的参数.append(self.executor.ctypes.data)
        return 调用算子时传入的参数, workspace

    def 根据输入构建GetWorkspaceSize参数类型(self):
        获取workspace函数的参数类型 = []
        for arg in self.参数保持不被销毁缓存:
            if (isinstance(arg, 张量)
                    or isinstance(arg, 张量列表)
                    or isinstance(arg, 标量)
                    or isinstance(arg, 标量数组)
                    or isinstance(arg, 数组)):
                获取workspace函数的参数类型.append(ctypes.c_void_p)
            elif isinstance(arg, bool):
                获取workspace函数的参数类型.append(ctypes.c_bool)
            elif isinstance(arg, int):
                int32_info = np.iinfo(np.int32)
                if arg > int32_info.max or arg < int32_info.min:
                    获取workspace函数的参数类型.append(ctypes.c_int64)
                else:
                    获取workspace函数的参数类型.append(ctypes.c_int32)
            elif isinstance(arg, float):
                float32_info = np.finfo(np.float32)
                if arg > float32_info.max or arg < float32_info.min:
                    获取workspace函数的参数类型.append(ctypes.c_double)
                else:
                    获取workspace函数的参数类型.append(ctypes.c_float)
            elif isinstance(arg, bytes):
                获取workspace函数的参数类型.append(ctypes.c_char_p)
            elif isinstance(arg, ctypes.c_int8):
                获取workspace函数的参数类型.append(ctypes.c_int8)
            elif isinstance(arg, ctypes.c_int16):
                获取workspace函数的参数类型.append(ctypes.c_int16)
            elif isinstance(arg, ctypes.c_int32):
                获取workspace函数的参数类型.append(ctypes.c_int32)
            elif isinstance(arg, ctypes.c_int64):
                获取workspace函数的参数类型.append(ctypes.c_int64)
            elif isinstance(arg, ctypes.c_uint8):
                获取workspace函数的参数类型.append(ctypes.c_uint8)
            elif isinstance(arg, ctypes.c_uint16):
                获取workspace函数的参数类型.append(ctypes.c_uint16)
            elif isinstance(arg, ctypes.c_uint32):
                获取workspace函数的参数类型.append(ctypes.c_uint32)
            elif isinstance(arg, ctypes.c_uint64):
                获取workspace函数的参数类型.append(ctypes.c_uint64)
            elif isinstance(arg, ctypes.c_float):
                获取workspace函数的参数类型.append(ctypes.c_float)
            elif isinstance(arg, ctypes.c_double):
                获取workspace函数的参数类型.append(ctypes.c_double)
        获取workspace函数的参数类型.append(ctypes.c_void_p)
        获取workspace函数的参数类型.append(ctypes.c_void_p)
        self.获取workspace大小函数.argtypes = 获取workspace函数的参数类型

    def 设置GetWorkspaceSize参数类型(self, 类型列表: list):
        self.获取workspace大小函数.argtypes = 类型列表

    def __call__(self, *args, 自动推导GetWorkspaceSize函数参数类型=True):
        self.根据输入将ndarray创建为张量并缓存参数(*args)
        调用算子时传入的参数, workspace = self.GetWorkspaceSize函数的参数()
        if 自动推导GetWorkspaceSize函数参数类型:
            self.根据输入构建GetWorkspaceSize参数类型()
        ret = self.获取workspace大小函数(*调用算子时传入的参数)
        记录acl返回值错误日志并抛出异常('获取workspace大小函数', ret)
        workspace指针 = 0
        workspace容量 = int(workspace[0])
        if workspace容量 > 0:
            self.workspace内存 = 设备内存(workspace容量)
            workspace指针 = self.workspace内存.指针
        self.算子执行函数(workspace指针, workspace容量, int(self.executor[0]), 0)
        记录acl返回值错误日志并抛出异常('算子执行函数', ret)
        return self.参数保持不被销毁缓存
