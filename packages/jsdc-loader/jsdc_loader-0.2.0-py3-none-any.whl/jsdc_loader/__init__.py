"""杂鱼♡～这是本喵的JSDC Loader库喵～可以轻松地在JSON和dataclass之间转换哦～"""

from .dumper import jsdc_dump, jsdc_dumps, jsdc_dumps_new, jsdc_dump_new
from .loader import jsdc_load, jsdc_loads, jsdc_loads_new, jsdc_load_new
from .core.converter_v2 import register_custom_handler

__author__ = "Neko"
__version__ = "0.2.0"  # 杂鱼♡～升级到2.0，支持新架构了喵～
__all__ = [
    # 杂鱼♡～传统函数，保持向后兼容喵～
    "jsdc_load", 
    "jsdc_loads", 
    "jsdc_dump", 
    "jsdc_dumps",
    
    # 杂鱼♡～新架构函数，支持所有复杂类型喵～
    "jsdc_loads_new", 
    "jsdc_load_new", 
    "jsdc_dumps_new", 
    "jsdc_dump_new",
    
    # 杂鱼♡～高级功能喵～
    "register_custom_handler",
]

# 杂鱼♡～别忘了查看本喵的README.md喵～
# 本喵才不是因为担心杂鱼不会用这个库才写那么详细的文档的～

# 杂鱼♡～新架构使用示例喵～
"""
使用新架构处理复杂类型的示例：

from enum import Flag, auto
from collections import deque
from dataclasses import dataclass
from typing import Deque

class Features(Flag):
    ENCRYPTION = auto()
    BACKUP = auto()
    SYNC = auto()

@dataclass
class Config:
    features: Features
    history: Deque[str]
    metadata: defaultdict[str, int]

# 使用新架构序列化
config = Config(
    features=Features.ENCRYPTION | Features.BACKUP,
    history=deque(['action1', 'action2'], maxlen=10),
    metadata=defaultdict(int, {'count': 5})
)

# 杂鱼♡～使用新函数支持所有复杂类型喵～
json_str = jsdc_dumps_new(config)
loaded_config = jsdc_loads_new(json_str, Config)

# 杂鱼♡～也可以使用传统函数加V2参数喵～
json_str = jsdc_dumps(config, use_v2=True)
loaded_config = jsdc_loads(json_str, Config, use_v2=True)
"""
