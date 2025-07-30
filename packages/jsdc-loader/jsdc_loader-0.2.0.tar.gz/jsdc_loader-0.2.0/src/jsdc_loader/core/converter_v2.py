"""杂鱼♡～这是本喵全新设计的转换器喵～使用插件式类型处理器系统，支持所有复杂类型～"""

import json
from typing import Any, Type, TypeVar
from dataclasses import is_dataclass

from .type_handlers import TypeHandlerRegistry

T = TypeVar('T')


def validate_target_type(target_type: Type) -> None:
    """杂鱼♡～验证目标类型是否有效喵～"""
    if not target_type:
        raise TypeError("杂鱼♡～目标类型不能为None喵！～")
    
    # 杂鱼♡～对于dataclass，需要特殊验证喵～
    if hasattr(target_type, '__origin__'):
        # 杂鱼♡～泛型类型，不做严格验证喵～
        return
    
    # 杂鱼♡～基本类型都是可以的喵～
    if target_type in (int, float, str, bool, list, dict, set, tuple, type(None)):
        return
    
    # 杂鱼♡～typing模块的类型也都是可以的喵～
    if hasattr(target_type, '__module__') and target_type.__module__ == 'typing':
        return
    
    # 杂鱼♡～如果是dataclass也是可以的喵～
    if is_dataclass(target_type):
        return
    
    # 杂鱼♡～其他类型暂时也允许，让处理器系统来处理喵～


class JSConverterV2:
    """杂鱼♡～新版本的JSON序列化转换器喵～使用处理器系统架构～"""
    
    def __init__(self):
        """杂鱼♡～初始化转换器喵～"""
        self.registry = TypeHandlerRegistry()
    
    def object_to_dict(self, obj: Any, obj_type: Type = None) -> dict:
        """杂鱼♡～将对象转换为字典格式喵～"""
        if obj_type is None:
            obj_type = type(obj)
        
        # 杂鱼♡～使用处理器系统进行序列化喵～
        serialized_data = self.registry.serialize(obj, obj_type)
        
        # 杂鱼♡～如果返回的不是字典，需要包装一下喵～
        if not isinstance(serialized_data, dict):
            return {
                "__root_value__": serialized_data,
                "__root_type__": f"{obj_type.__module__}.{obj_type.__name__}" if hasattr(obj_type, '__name__') else str(obj_type)
            }
        
        return serialized_data
    
    def dict_to_object(self, data: dict, target_type: Type[T]) -> T:
        """杂鱼♡～将字典转换为目标类型对象喵～"""
        # 杂鱼♡～处理根值类型喵～
        if "__root_value__" in data and "__root_type__" in data:
            root_value = data["__root_value__"]
            return self.registry.deserialize(root_value, target_type)
        
        # 杂鱼♡～使用处理器系统进行反序列化喵～
        return self.registry.deserialize(data, target_type)
    
    def dumps(self, obj: Any, obj_type: Type = None, indent: int = 4) -> str:
        """杂鱼♡～序列化对象为JSON字符串喵～"""
        try:
            # 杂鱼♡～转换为字典格式喵～
            data_dict = self.object_to_dict(obj, obj_type)
            
            # 杂鱼♡～序列化为JSON字符串喵～
            json_str = json.dumps(data_dict, indent=indent, ensure_ascii=False)
            return json_str
            
        except (ValueError, TypeError) as e:
            # 杂鱼♡～让类型和值错误直接传播，这是期望的行为喵～
            raise e
        except Exception as e:
            raise RuntimeError(f"杂鱼♡～序列化失败了喵～: {str(e)}") from e
    
    def loads(self, json_str: str, target_type: Type[T]) -> T:
        """杂鱼♡～从JSON字符串反序列化对象喵～"""
        try:
            # 杂鱼♡～解析JSON字符串喵～
            data = json.loads(json_str)
            
            # 杂鱼♡～验证目标类型喵～
            validate_target_type(target_type)
            
            # 杂鱼♡～转换为目标对象喵～
            return self.dict_to_object(data, target_type)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"杂鱼♡～JSON格式错误喵～: {str(e)}") from e
        except (ValueError, TypeError) as e:
            # 杂鱼♡～让类型和值错误直接传播，这是期望的行为喵～
            raise e
        except Exception as e:
            raise RuntimeError(f"杂鱼♡～反序列化失败了喵～: {str(e)}") from e


# 杂鱼♡～创建全局转换器实例喵～
_converter_v2 = JSConverterV2()


def jsdc_dumps_v2(obj: Any, obj_type: Type = None, indent: int = 4) -> str:
    """杂鱼♡～新版本序列化函数喵～支持所有复杂类型～
    
    Args:
        obj: 要序列化的对象
        obj_type: 对象类型（可选）
        indent: JSON缩进空格数
        
    Returns:
        JSON字符串
        
    Examples:
        >>> from enum import Flag, auto
        >>> from collections import deque
        >>> 
        >>> class Features(Flag):
        ...     ENCRYPTION = auto()
        ...     BACKUP = auto()
        ...
        >>> @dataclass
        >>> class Config:
        ...     features: Features
        ...     history: Deque[str]
        ...
        >>> config = Config(Features.ENCRYPTION | Features.BACKUP, deque(['a', 'b']))
        >>> json_str = jsdc_dumps_v2(config)
        >>> print(json_str)
    """
    return _converter_v2.dumps(obj, obj_type, indent)


def jsdc_loads_v2(json_str: str, target_type: Type[T]) -> T:
    """杂鱼♡～新版本反序列化函数喵～支持所有复杂类型～
    
    Args:
        json_str: JSON字符串
        target_type: 目标类型
        
    Returns:
        反序列化的对象
        
    Examples:
        >>> config = jsdc_loads_v2(json_str, Config)
        >>> assert isinstance(config.features, Features)
        >>> assert isinstance(config.history, deque)
    """
    return _converter_v2.loads(json_str, target_type)


def register_custom_handler(handler):
    """杂鱼♡～注册自定义类型处理器喵～
    
    Args:
        handler: 继承自TypeHandler的自定义处理器
        
    Examples:
        >>> class MyCustomHandler(TypeHandler):
        ...     def can_handle(self, obj, target_type):
        ...         return isinstance(obj, MyCustomType)
        ...     # 实现其他方法...
        >>> 
        >>> register_custom_handler(MyCustomHandler())
    """
    _converter_v2.registry.register_handler(handler)


# 杂鱼♡～为了向后兼容，也提供简单的函数别名喵～
dumps_v2 = jsdc_dumps_v2
loads_v2 = jsdc_loads_v2 