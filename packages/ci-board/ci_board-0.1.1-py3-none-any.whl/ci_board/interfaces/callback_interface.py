# 杂鱼♡～本喵设计的回调接口定义喵～
from abc import ABC, abstractmethod
from typing import Callable, Generic, List, Optional, TypeVar

from ..core.deduplicator import Deduplicator
from ..types.t_source import ProcessInfo
from ..utils.logger import get_component_logger

T = TypeVar("T")


class CallbackInterface(Generic[T], ABC):
    """杂鱼♡～抽象的回调接口，所有处理器都要继承这个喵～"""

    @abstractmethod
    def get_interested_formats(self) -> List[int]:
        """杂鱼♡～告诉本喵你对哪些剪贴板格式感兴趣喵～"""
        pass

    @abstractmethod
    def process_data(self, format_id: int, handle: int, source_info: Optional[ProcessInfo]) -> None:
        """
        杂鱼♡～处理原始剪贴板数据的抽象方法喵～
        你得自己锁内存、读数据、解锁，哼～
        """
        pass

    def handle(self, data: T, source_info: Optional[ProcessInfo] = None) -> None:
        """
        杂鱼♡～处理剪贴板数据的抽象方法喵～
        （这个方法很快就要被废弃了喵，哼～）
        """
        pass

    def is_valid(self, data: T) -> bool:
        """
        杂鱼♡～检查数据是否有效的抽象方法喵～
        （这个方法也快没用了喵～）
        """
        return True


class BaseClipboardHandler(CallbackInterface[T]):
    """杂鱼♡～基础剪贴板处理器，提供通用功能喵～"""

    def __init__(self, callback: Optional[Callable] = None, deduplicator: Optional[Deduplicator] = None):
        """
        杂鱼♡～初始化处理器喵～

        Args:
            callback: 可选的回调函数
            deduplicator: 可选的去重器实例喵～
        """
        self._callback = callback
        self._deduplicator = deduplicator
        self._enabled = True
        self._include_source_info = True  # 杂鱼♡～默认包含源信息喵～
        self.logger = get_component_logger(
            f"handler.{self.__class__.__name__.lower()}"
        )

    def set_callback(self, callback: callable) -> None:
        """杂鱼♡～设置回调函数喵～"""
        self._callback = callback

    def enable_source_info(self) -> None:
        """杂鱼♡～启用源应用信息喵～"""
        self._include_source_info = True

    def disable_source_info(self) -> None:
        """杂鱼♡～禁用源应用信息喵～"""
        self._include_source_info = False

    def enable(self) -> None:
        """杂鱼♡～启用处理器喵～"""
        self._enabled = True

    def disable(self) -> None:
        """杂鱼♡～禁用处理器喵～"""
        self._enabled = False

    def is_enabled(self) -> bool:
        """杂鱼♡～检查处理器是否启用喵～"""
        return self._enabled

    def handle(self, data: T, source_info: Optional[ProcessInfo] = None) -> None:
        """杂鱼♡～处理数据的通用方法喵～"""
        if not self._enabled:
            return

        if not self.is_valid(data):
            return

        if self._callback:
            # 杂鱼♡～本喵会帮你检查回调函数需不需要源信息喵～
            import inspect

            try:
                sig = inspect.signature(self._callback)
                if len(sig.parameters) >= 2:
                    self._callback(
                        data, source_info if self._include_source_info else None
                    )
                else:
                    self._callback(data)
            except (ValueError, TypeError):
                # 杂鱼♡～如果获取签名失败，就默认只传数据喵～
                self._callback(data)

        else:
            self._default_handle(data, source_info)

    @abstractmethod
    def _default_handle(
        self, data: T, source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认处理方法，子类必须重写喵～"""
        # 杂鱼♡～子类应该重写这个方法并使用自己的logger喵～
        self.logger.info(f"杂鱼♡～处理数据：{str(data)[:100]}")
        if source_info and self._include_source_info:
            self.logger.info(
                f"杂鱼♡～源应用程序：{source_info.process_name} ({source_info.process_path})"
            )
