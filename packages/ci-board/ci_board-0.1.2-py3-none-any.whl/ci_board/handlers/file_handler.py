# 杂鱼♡～本喵的文件处理器喵～
import os
import ctypes
from typing import Callable, List, Optional

from ci_board.interfaces import BaseClipboardHandler
from ci_board.types import FileInfo, ProcessInfo
from ci_board.utils import get_component_logger
from ..utils.win32_api import ClipboardFormat, Win32API

# 杂鱼♡～获取组件专用logger喵～
logger = get_component_logger("handlers.file_handler")


class FileHandler(BaseClipboardHandler[List[str]]):
    """杂鱼♡～专门处理文件的处理器喵～"""

    def __init__(
        self,
        callback: Optional[Callable[[List[str], Optional[ProcessInfo]], None]] = None,
    ):
        """
        杂鱼♡～初始化文件处理器喵～

        Args:
            callback: 处理文件列表的回调函数, 接收 (files, source_info)
        """
        super().__init__(callback)

    def is_valid(self, data: Optional[List[str]] = None) -> bool:
        """杂鱼♡～检查文件数据是否有效喵～"""
        if not isinstance(data, list) or not data:
            return False

        # 杂鱼♡～检查每个文件路径喵～
        for file_path in data:
            if not isinstance(file_path, str) or not os.path.exists(file_path):
                self.logger.warning(f"文件路径无效或不存在: {file_path}")
                return False

        return True

    def get_interested_formats(self) -> List[int]:
        """杂鱼♡～本喵只对文件列表（HDROP）感兴趣喵～"""
        return [ClipboardFormat.CF_HDROP.value]

    def process_data(self, format_id: int, handle: int, source_info: Optional[ProcessInfo]) -> None:
        """杂鱼♡～处理文件列表的原始数据句柄喵～"""
        if not self._enabled:
            return

        file_list = self._read_files_from_handle(handle)
        if not file_list:
            return

        if self._callback:
            try:
                import inspect
                sig = inspect.signature(self._callback)
                if len(sig.parameters) >= 2:
                    self._callback(file_list, source_info if self._include_source_info else None)
                else:
                    self._callback(file_list)
            except (ValueError, TypeError):
                self._callback(file_list)
        else:
            self._default_handle(file_list, source_info)

    def _read_files_from_handle(self, handle: int) -> Optional[List[str]]:
        """杂鱼♡～从HDROP句柄里解析出文件列表喵～"""
        try:
            file_count = Win32API.shell32.DragQueryFileW(handle, 0xFFFFFFFF, None, 0)
            if file_count == 0:
                return []

            files = []
            for i in range(file_count):
                buffer_size = Win32API.shell32.DragQueryFileW(handle, i, None, 0) + 1
                buffer = ctypes.create_unicode_buffer(buffer_size)
                Win32API.shell32.DragQueryFileW(handle, i, buffer, buffer_size)
                files.append(buffer.value)
            return files
        except Exception as e:
            self.logger.error(f"解析HDROP句柄失败喵: {e}", exc_info=True)
            return None

    def _default_handle(
        self, data: List[str], source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认的文件处理方法喵～"""
        self.logger.info("杂鱼♡～检测到文件变化喵：")
        self.logger.info(f"  文件数量：{len(data)}")

        for i, file_path in enumerate(data, 1):
            self.logger.info(f"  文件{i}：{file_path}")

        if source_info and self._include_source_info:
            process_name = source_info.process_name or "Unknown"
            if process_name == "Unknown":
                self.logger.warning("  源应用程序：❓ 未知 (无法获取)")
            else:
                self.logger.info(f"  源应用程序：{process_name}")
            if source_info.process_path and process_name != "Unknown":
                self.logger.debug(f"  程序路径：{source_info.process_path}")
        self.logger.info("-" * 50)

    def get_file_info(self, file_path: str) -> Optional[FileInfo]:
        """杂鱼♡～获取文件信息喵～"""
        import datetime
        import os

        if not os.path.exists(file_path):
            return None

        try:
            stat = os.stat(file_path)
            return FileInfo(
                path=file_path,
                name=os.path.basename(file_path),
                directory=os.path.dirname(file_path),
                extension=os.path.splitext(file_path)[1],
                exists=True,
                size=self._format_file_size(stat.st_size),
                modified=str(datetime.datetime.fromtimestamp(stat.st_mtime)),
            )
        except OSError as e:
            self.logger.error(f"获取文件信息失败喵: {file_path}, 错误: {e}")
            return None

    def _format_file_size(self, size_bytes: int) -> str:
        """杂鱼♡～格式化文件大小喵～"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math

        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
