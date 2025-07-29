# 杂鱼♡～本喵设计的剪贴板监控包喵～
"""
杂鱼♡～本喵的剪贴板监控包 v0.1.2
一个高扩展性的、模块化的剪贴板监控解决方案喵～
"""

from .core.monitor import ClipboardMonitor
from .handlers import FileHandler, ImageHandler, TextHandler
from .interfaces import BaseClipboardHandler, CallbackInterface
from .types import BMPData, DIBData, FileInfo, ProcessInfo

__author__ = "Neko"
__version__ = "0.1.2"  # 杂鱼♡～版本升级了喵！

# 杂鱼♡～导出主要API，让杂鱼主人使用方便喵～


# 杂鱼♡～提供简单的函数式API给懒惰的杂鱼主人喵～
def create_monitor(
    async_processing: bool = True,
    max_workers: int = 4,
    handler_timeout: float = 30.0,
    enable_source_tracking: bool = True,
):
    """
    杂鱼♡～创建一个新的剪贴板监控器实例喵～

    Args:
        async_processing: 是否启用异步处理模式（默认True）
        max_workers: 处理器线程池最大工作线程数（默认4）
        handler_timeout: 单个处理器超时时间，秒（默认30.0）
        enable_source_tracking: 是否启用源应用追踪（默认True）
    """
    return ClipboardMonitor(
        async_processing=async_processing,
        max_workers=max_workers,
        handler_timeout=handler_timeout,
        enable_source_tracking=enable_source_tracking,
    )


def create_text_handler(callback=None) -> TextHandler:
    """杂鱼♡～创建文本处理器喵～"""
    return TextHandler(callback)


def create_image_handler(callback=None) -> ImageHandler:
    """杂鱼♡～创建图片处理器喵～"""
    return ImageHandler(callback)


def create_file_handler(callback=None) -> FileHandler:
    """杂鱼♡～创建文件处理器喵～"""
    return FileHandler(callback)


# 杂鱼♡～导出所有重要的类和函数喵～
__all__ = [
    # 杂鱼♡～主要工厂函数喵～
    "create_monitor",
    # 杂鱼♡～处理器类和它们的工厂函数喵～
    "TextHandler",
    "ImageHandler",
    "FileHandler",
    "create_text_handler",
    "create_image_handler",
    "create_file_handler",
    # 杂鱼♡～处理器接口，方便高级杂鱼主人自定义喵～
    "CallbackInterface",
    "BaseClipboardHandler",
    # 杂鱼♡～数据类型喵～
    "BMPData",
    "DIBData",
    "FileInfo",
    "ProcessInfo",
]
