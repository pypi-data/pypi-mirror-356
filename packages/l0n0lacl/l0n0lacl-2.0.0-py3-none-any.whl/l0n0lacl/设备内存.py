import acl
from .日志 import 记录acl返回值错误日志并抛出异常
from typing import Union


class 内存分配方案:
    """
    0：ACL_MEM_MALLOC_HUGE_FIRST，当申请的内存小于等于1M时，即使使用该内存分配规则，也是申请普通页的内存。当申请的内存大于1M时，优先申请大页内存，如果大页内存不够，则使用普通页的内存。
    1：ACL_MEM_MALLOC_HUGE_ONLY，仅申请大页，如果大页内存不够，则返回错误。
    2：ACL_MEM_MALLOC_NORMAL_ONLY，仅申请普通页。
    3：ACL_MEM_MALLOC_HUGE_FIRST_P2P，仅Device之间内存复制场景下申请内存时使用该选项，表示优先申请大页内存，如果大页内存不够，则使用普通页的内存。预留选项。
    4：ACL_MEM_MALLOC_HUGE_ONLY_P2P，仅Device之间内存复制场景下申请内存时使用该选项，仅申请大页内存，如果大页内存不够，则返回错误。预留选项。
    5：ACL_MEM_MALLOC_NORMAL_ONLY_P2P，仅Device之间内存复制场景下申请内存时使用该选项，仅申请普通页的内存。预留选项。
    """
    大页优先_小于1M普通页_大于1M优先使用大页 = 0
    仅分配大页_大页不够_返回错误 = 1
    仅分配普通页 = 2
    设备之间复制时使用的大页优先策略 = 3
    设备之间复制时使用的仅申请大页 = 4
    设备之间复制时使用的仅申请普通页 = 5
    ACL_MEM_TYPE_LOW_BAND_WIDTH = 0x0100
    ACL_MEM_TYPE_HIGH_BAND_WIDTH = 0x1000


class 内存复制类型:
    主机到主机 = 0
    主机到设备 = 1
    设备到主机 = 2
    设备到设备 = 3


class 设备内存:
    def __init__(self, 内存大小: int, 策略: Union[int, None] = None):
        self.内存大小 = 内存大小
        self.设备内存指针, ret = acl.rt.malloc(
            内存大小, 策略 or 内存分配方案.大页优先_小于1M普通页_大于1M优先使用大页)
        记录acl返回值错误日志并抛出异常("分配内存失败", ret)

    def __del__(self):
        if self.设备内存指针 is None:
            return
        acl.rt.free(self.设备内存指针)

    @property
    def 指针(self):
        return self.设备内存指针

    def 从主机复制数据(self, 主机内存指针: int, 要复制的数据大小: int):
        要复制的数据大小 = int(min(要复制的数据大小, self.内存大小))
        ret = acl.rt.memcpy(
            self.设备内存指针,
            要复制的数据大小,
            主机内存指针,
            要复制的数据大小,
            内存复制类型.主机到设备,
        )
        记录acl返回值错误日志并抛出异常("AclMemory memcpy", ret)

    def 将数据复制到主机(self, 主机内存指针: int, 要复制的数据大小: int):
        要复制的数据大小 = int(min(要复制的数据大小, self.内存大小))
        ret = acl.rt.memcpy(
            主机内存指针,
            要复制的数据大小,
            self.设备内存指针,
            要复制的数据大小,
            内存复制类型.设备到主机,
        )
        记录acl返回值错误日志并抛出异常("AclMemory memcpy", ret)

    def 从设备复制数据(self, 设备内存指针: int, 要复制的数据大小: int):
        要复制的数据大小 = int(min(要复制的数据大小, self.内存大小))
        ret = acl.rt.memcpy(
            self.设备内存指针,
            要复制的数据大小,
            设备内存指针,
            要复制的数据大小,
            内存复制类型.设备到设备,
        )
        记录acl返回值错误日志并抛出异常("AclMemory memcpy", ret)

    def 将数据复制到设备(self, 设备内存指针: int, 要复制的数据大小: int):
        要复制的数据大小 = int(min(要复制的数据大小, self.内存大小))
        ret = acl.rt.memcpy(
            设备内存指针,
            要复制的数据大小,
            self.设备内存指针,
            要复制的数据大小,
            内存复制类型.设备到设备,
        )
        记录acl返回值错误日志并抛出异常("AclMemory memcpy", ret)
