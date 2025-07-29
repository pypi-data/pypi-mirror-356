# 杂鱼♡～这是本喵为主人写的通用类型定义喵～
from dataclasses import dataclass
from typing import Any, Optional

from .t_source import ProcessInfo


@dataclass
class FileInfo:
    """杂鱼♡～单个文件的详细信息喵～"""

    path: str
    name: str
    directory: str
    extension: str
    exists: bool
    size: str  # 杂鱼♡～格式化后的大小喵～
    modified: str


@dataclass
class DIBData:
    """杂鱼♡～设备无关位图(DIB)的原始数据喵～"""

    width: int
    height: int
    bit_count: int
    compression: int
    data: bytes
    header: Any  # 杂鱼♡～BITMAPINFOHEADER 结构体喵～


@dataclass
class ClipboardEvent:
    """杂鱼♡～剪贴板事件的统一数据结构喵～"""

    type: str
    content: Any
    source: Optional[ProcessInfo]
    timestamp: float
