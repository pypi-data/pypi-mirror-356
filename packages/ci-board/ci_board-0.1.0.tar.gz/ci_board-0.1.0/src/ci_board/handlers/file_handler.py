# 杂鱼♡～本喵的文件处理器喵～
import os
from typing import Callable, List, Optional

from ..interfaces.callback_interface import BaseClipboardHandler
from ..types import FileInfo, ProcessInfo
from ..utils.logger import get_component_logger

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

    def _default_handle(
        self, data: List[str], source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认的文件处理方法喵～"""
        self.logger.info("杂鱼♡～检测到文件变化喵：")
        self.logger.info(f"  文件数量：{len(data)}")

        for i, file_path in enumerate(data, 1):
            try:
                file_info = self.get_file_info(file_path)
                if file_info:
                    self.logger.info(f"  文件{i}：{file_info.name} ({file_info.size})")
            except Exception as e:
                self.logger.error(f"  获取文件信息失败喵: {file_path}, 错误: {e}")

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
