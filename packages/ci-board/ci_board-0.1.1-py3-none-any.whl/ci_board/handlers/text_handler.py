# 杂鱼♡～本喵的文本处理器喵～
import ctypes
from typing import Callable, List, Optional

from ..interfaces.callback_interface import BaseClipboardHandler
from ..types import ProcessInfo
from ..utils.win32_api import ClipboardFormat, Win32API
from ci_board.utils import get_component_logger
from ci_board.core.deduplicator import Deduplicator

# 杂鱼♡～获取组件专用logger喵～
logger = get_component_logger("handlers.text_handler")


class TextHandler(BaseClipboardHandler[str]):
    """杂鱼♡～专门处理文本的处理器喵～"""

    def __init__(self, callback: Optional[Callable] = None, deduplicator: Optional[Deduplicator] = None):
        """
        杂鱼♡～初始化文本处理器喵～

        Args:
            callback: 处理文本的回调函数
            deduplicator: 去重器实例
        """
        super().__init__(callback, deduplicator)

    def get_interested_formats(self) -> List[int]:
        """杂鱼♡～本喵只对Unicode文本感兴趣喵～"""
        return [ClipboardFormat.UNICODETEXT.value]

    def process_data(self, format_id: int, handle: int, source_info: Optional[ProcessInfo]) -> None:
        """杂鱼♡～处理文本的原始数据句柄喵～"""
        if not self._enabled:
            return

        text = self._read_text_from_handle(handle)
        if not text or not self._is_valid_text(text):
            return

        # 杂鱼♡～在处理前，先用本喵的去重器检查一下喵！～
        if self._deduplicator and self._deduplicator.is_duplicate('text', text):
            return

        if self._callback:
            try:
                import inspect
                sig = inspect.signature(self._callback)
                if len(sig.parameters) >= 2:
                    self._callback(text, source_info if self._include_source_info else None)
                else:
                    self._callback(text)
            except (ValueError, TypeError):
                self._callback(text)
        else:
            self._default_handle(text, source_info)

    def _read_text_from_handle(self, handle: int) -> Optional[str]:
        """杂鱼♡～从句柄读取文本喵～"""
        try:
            ptr = Win32API.kernel32.GlobalLock(handle)
            if not ptr:
                return None
            try:
                text = ctypes.wstring_at(ptr)
                return text
            finally:
                Win32API.kernel32.GlobalUnlock(handle)
        except Exception as e:
            self.logger.error(f"读取文本句柄失败喵: {e}", exc_info=True)
            return None

    def _is_valid_text(self, data: str) -> bool:
        """杂鱼♡～检查文本数据是否有效喵～"""
        return bool(data and data.strip())

    def _default_handle(
        self, data: str, source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认的文本处理方法喵～"""
        self.logger.info("杂鱼♡～检测到文本变化喵：")
        self.logger.info(f"  内容长度：{len(data)} 字符")
        self.logger.info(f"  前50个字符：{data[:50]}...")

        # 杂鱼♡～显示源应用程序信息喵～
        if source_info and self._include_source_info:
            process_name = source_info.process_name or "Unknown"

            # 杂鱼♡～根据不同情况显示不同的信息喵～
            if process_name == "Unknown":
                self.logger.warning("  源应用程序：❓ 未知 (无法获取)")
            else:
                self.logger.info(f"  源应用程序：{process_name}")

            # 杂鱼♡～显示其他详细信息喵～
            if source_info.process_path and process_name != "Unknown":
                self.logger.debug(f"  程序路径：{source_info.process_path}")
            if source_info.window_title:
                self.logger.debug(f"  窗口标题：{source_info.window_title}")
            if source_info.process_id:
                self.logger.debug(f"  进程ID：{source_info.process_id}")

        self.logger.info("-" * 50)
