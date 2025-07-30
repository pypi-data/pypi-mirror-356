"""杂鱼♡～这是本喵为你写的JSDC Loader的加载函数喵～本喵可是很擅长把JSON变成对象呢～"""

import json
from pathlib import Path
from typing import Optional, Type, Union

from .core import T, convert_dict_to_dataclass, validate_dataclass
from .core.converter_v2 import jsdc_loads_v2
from .file_ops import check_file_size


def jsdc_load(
    file_path: Union[str, Path],
    target_class: Type[T],
    encoding: str = "utf-8",
    max_file_size: Optional[int] = None,
    use_v2: bool = False,
) -> T:
    """杂鱼♡～本喵帮你从JSON文件加载数据并转换为指定的dataclass喵～

    Args:
        file_path (Union[str, Path]): JSON文件的路径喵～杂鱼现在可以用字符串或Path对象了♡～
        target_class (Type[T]): 目标dataclass类喵～
        encoding (str, optional): 文件编码，默认'utf-8'喵～
        max_file_size (Optional[int], optional): 最大文件大小（字节）喵～为None表示不限制～
        use_v2 (bool, optional): 是否使用新的V2架构喵～默认False保持兼容性～

    Returns:
        T: 从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        FileNotFoundError: 如果文件不存在喵～杂鱼肯定是路径搞错了～
        ValueError: 如果文件内容无效或太大喵～杂鱼的数据有问题吧～
        TypeError: 如果target_class不是dataclass，杂鱼肯定传错类型了～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{path}～")

    # 检查文件大小喵～
    if max_file_size is not None:
        check_file_size(str(path), max_file_size)

    try:
        with path.open("r", encoding=encoding) as f:
            json_str = f.read()

        # 如果数据为空，杂鱼肯定是犯了错误喵～
        if not json_str:
            raise ValueError("杂鱼♡～JSON文件为空喵！～")

        # 杂鱼♡～使用对应的加载方法喵～
        return jsdc_loads(json_str, target_class, use_v2)

    except UnicodeDecodeError as e:
        raise ValueError(
            f"杂鱼♡～用{encoding}解码失败喵：{str(e)}～杂鱼是不是编码搞错了？～"
        )
    except Exception as e:
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")


def jsdc_loads(json_str: str, target_class: Type[T], use_v2: bool = False) -> T:
    """杂鱼♡～本喵帮你从JSON字符串加载数据并转换为指定的dataclass喵～

    Args:
        json_str (str): JSON字符串喵～杂鱼提供的内容要合法哦～
        target_class (Type[T]): 目标dataclass类喵～
        use_v2 (bool, optional): 是否使用新的V2架构喵～默认False保持兼容性～

    Returns:
        T: 从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        ValueError: 如果字符串内容无效喵～杂鱼的数据有问题吧～
        TypeError: 如果target_class不是dataclass，杂鱼肯定传错类型了～
    """
    if not json_str:
        raise ValueError("杂鱼♡～JSON字符串为空喵！～")

    # 杂鱼♡～如果使用V2架构，直接调用新的处理器系统喵～
    if use_v2:
        return jsdc_loads_v2(json_str, target_class)

    # 验证目标类喵～
    validate_dataclass(target_class)

    try:
        json_data = json.loads(json_str)

        # 如果数据为空，杂鱼肯定是犯了错误喵～
        if not json_data:
            raise ValueError("杂鱼♡～JSON数据为空喵！～")

        # 转换数据为目标类型喵～
        return convert_dict_to_dataclass(json_data, target_class)
    except json.JSONDecodeError as e:
        raise ValueError(f"杂鱼♡～无效的JSON喵：{str(e)}～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")


# 杂鱼♡～为了方便使用新架构，本喵提供专门的V2函数喵～
def jsdc_load_new(
    file_path: Union[str, Path],
    target_class: Type[T],
    encoding: str = "utf-8",
    max_file_size: Optional[int] = None,
) -> T:
    """杂鱼♡～使用新架构的文件加载函数喵～支持所有复杂类型～
    
    这是jsdc_load的V2版本，使用新的插件式类型处理器系统喵～
    支持Flag、IntFlag、Deque、FrozenSet、defaultdict、Generic、Literal等复杂类型～
    
    Args:
        file_path (Union[str, Path]): JSON文件路径喵～
        target_class (Type[T]): 目标类喵～
        encoding (str, optional): 文件编码喵～默认'utf-8'～
        max_file_size (Optional[int], optional): 最大文件大小限制喵～
        
    Returns:
        T: 反序列化的对象喵～
        
    Examples:
        >>> from enum import Flag, auto
        >>> from collections import deque
        >>> @dataclass
        >>> class Config:
        ...     features: Flag
        ...     history: Deque[str]
        >>> config = jsdc_load_new("config.json", Config)
        >>> assert isinstance(config.features, Flag)
        >>> assert isinstance(config.history, deque)
    """
    return jsdc_load(file_path, target_class, encoding, max_file_size, use_v2=True)


def jsdc_loads_new(json_str: str, target_class: Type[T]) -> T:
    """杂鱼♡～使用新架构的字符串加载函数喵～支持所有复杂类型～
    
    这是jsdc_loads的V2版本，使用新的插件式类型处理器系统喵～
    
    Args:
        json_str (str): JSON字符串喵～
        target_class (Type[T]): 目标类喵～
        
    Returns:
        T: 反序列化的对象喵～
        
    Examples:
        >>> json_str = '{"features": 5, "history": {"__type__": "deque", "__data__": ["a", "b"]}}'
        >>> config = jsdc_loads_new(json_str, Config)
    """
    return jsdc_loads_v2(json_str, target_class)
