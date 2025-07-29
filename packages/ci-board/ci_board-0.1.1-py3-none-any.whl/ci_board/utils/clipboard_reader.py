# 杂鱼♡～本喵为杂鱼主人创建的剪贴板数据读取器喵～
import threading
from typing import List, Optional

from .logger import get_component_logger
from .win32_api import Win32API


class ClipboardReader:
    """
    杂鱼♡～专门负责读取剪贴板原始数据的类喵～
    本喵只负责打开、关闭和拿出指定格式的数据句柄，才不管里面是什么东西！
    """

    def __init__(self):
        self._clipboard_lock = threading.RLock()
        self._logger = get_component_logger("utils.clipboard_reader")

    def get_available_formats(self) -> List[int]:
        """杂鱼♡～获取剪贴板上所有可用的格式ID喵～"""
        formats = []
        with self._clipboard_lock:
            try:
                if not Win32API.user32.OpenClipboard(None):
                    self._logger.warning("无法打开剪贴板来枚举格式喵！")
                    return []

                current_format = 0
                while True:
                    # 杂鱼♡～循环调用来获取所有格式喵～
                    current_format = Win32API.user32.EnumClipboardFormats(current_format)
                    if current_format == 0:
                        # 杂鱼♡～没有更多格式了，或者出错了喵～
                        last_error = Win32API.kernel32.GetLastError()
                        if last_error != 0:
                            self._logger.error(f"枚举剪贴板格式失败喵，错误码: {last_error}")
                        break
                    formats.append(current_format)

            finally:
                Win32API.user32.CloseClipboard()
        return formats

    def get_handle_for_format(self, format_id: int) -> Optional[int]:
        """
        杂鱼♡～获取指定格式的数据句柄喵～
        哼，本喵只给你句柄，怎么用是你的事！
        """
        handle = None
        with self._clipboard_lock:
            try:
                if not Win32API.user32.OpenClipboard(None):
                    self._logger.warning(f"无法打开剪贴板来获取格式 {format_id} 的句柄！")
                    return None

                handle = Win32API.user32.GetClipboardData(format_id)
                if not handle:
                    self._logger.debug(f"格式 {format_id} 的数据句柄为空喵。")

            except Exception as e:
                self._logger.error(f"获取格式 {format_id} 句柄时出错: {e}", exc_info=True)
                handle = None   # 确保出错了就返回None
            finally:
                Win32API.user32.CloseClipboard()

        return handle
