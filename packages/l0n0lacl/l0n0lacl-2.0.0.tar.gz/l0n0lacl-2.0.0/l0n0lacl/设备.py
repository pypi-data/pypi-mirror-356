import acl
import os
from .日志 import 记录acl返回值错误日志并抛出异常
from typing import Union


class 设备信息:
    AICore数量 = 0
    VectorCore数量 = 1
    L2Buffer大小 = 2


class 设备管理器:
    def __init__(self) -> None:
        self.初始化成功 = False
        设备ID字符串 = os.environ.get("ASCEND_VISIBLE_DEVICES")
        if 设备ID字符串 is None:
            raise Exception("环境变量ASCEND_VISIBLE_DEVICES未设置")
        self.设备IDS = [int(ID) for ID in 设备ID字符串.strip().split(',')]
        self.__初始化上下文与执行流水线()
        self.初始化成功 = True

    def __del__(self):
        for 设备ID in self.设备IDS:
            ret = acl.rt.reset_device(设备ID)
            记录acl返回值错误日志并抛出异常(f'acl.rt.reset_device({设备ID}))', ret)

    def __初始化上下文与执行流水线(self):
        for i in range(self.设备数量 - 1, -1, -1):
            self._设置当前设备(i)

    @property
    def 设备数量(self):
        return len(self.设备IDS)

    @property
    def 当前设备索引(self):
        当前设备ID, ret = acl.rt.get_device()
        记录acl返回值错误日志并抛出异常(f'acl.rt.get_device())', ret)
        return self.设备IDS.index(当前设备ID)

    def _设备信息(self, 设备索引: int, 信息类型: int):
        设备ID = self.设备IDS[设备索引]
        value, ret = acl.get_device_capability(设备ID, 信息类型)
        记录acl返回值错误日志并抛出异常(f'acl.get_device_capability(设备ID, {信息类型})', ret)
        return value

    def 设备AICore数量(self, 设备索引: int):
        return self._设备信息(设备索引, 设备信息.AICore数量)

    def 设备VectorCore数量(self, 设备索引: int):
        return self._设备信息(设备索引, 设备信息.VectorCore数量)

    def 设备L2Buffer大小(self, 设备索引: int):
        return self._设备信息(设备索引, 设备信息.L2Buffer大小)

    def _设置当前设备(self, 设备索引: int):
        设备ID = self.设备IDS[设备索引]
        ret = acl.rt.set_device(设备ID)
        记录acl返回值错误日志并抛出异常(f'acl.set_device({设备ID})', ret)

    def 切换设备到(self, 设备索引: int):
        if self.初始化成功:
            if self.当前设备索引 == 设备索引:
                return
            self.同步当前设备流水()
        self._设置当前设备(设备索引)

    def 初始化目标设备(self, 目标, 设备索引: Union[int, None] = None):
        if 设备索引 is not None and self.当前设备索引 != 设备索引:
            目标.设备索引 = 设备索引
            self.切换设备到(设备索引)
        else:
            目标.设备索引 = self.当前设备索引

    def 同步当前设备流水(self):
        ret = acl.rt.synchronize_stream(0)
        记录acl返回值错误日志并抛出异常(f"acl.rt.synchronize_stream({0})", ret)
