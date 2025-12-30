# common.py 【数据定义处，全局所有模块都从这里导入】
from dataclasses import dataclass

# Temporal 服务器地址
TEMPORAL_HOST = "temporal-server:7233"

# Activity 参数定义
@dataclass
class ActParams:
    msg:                    str         # 数据
    fail_first_attempt:     bool        # 是否第一次失败

# 工作流输入定义
@dataclass
class InputJson:
    msg:                    str         # 数据
    fail_first_attempt:     bool        # 是否第一次失败

# 查询结果定义
@dataclass
class OutputJson:
    job_id:     str         # 数据
    status:     int         # 是否第一次失败
    start_time: str         # 开始时间
    end_time:   str         # 结束时间
    attempt:    int         # 尝试次数

# Activity 结果定义
@dataclass
class Result:
    msg:       str         # 数据
    attempt:    int         # 尝试次数