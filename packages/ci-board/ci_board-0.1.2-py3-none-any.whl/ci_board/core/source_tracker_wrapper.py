# 杂鱼♡～这是本喵为SourceTracker写的包装器喵～
import time
from typing import Any, Dict, Optional

from ci_board.types import ProcessInfo
from ci_board.utils import get_component_logger
from ci_board.core.source_tracker_ import SourceTracker as StaticSourceTracker


class SourceTrackerWrapper:
    """
    杂鱼♡～一个实例化的包装器，包住了静态的SourceTracker喵～
    本喵这样做是为了让代码更清晰，并且把字典转换成类型安全的ProcessInfo喵！
    """

    def __init__(self):
        self.logger = get_component_logger("core.source_tracker_wrapper")

    def initialize(self):
        """杂鱼♡～初始化底层的静态追踪器喵～"""
        self.logger.info("初始化源追踪器...")
        if not StaticSourceTracker.initialize_integrated_tracking():
            self.logger.warning("杂鱼♡～警告：集成式焦点跟踪初始化失败喵～")

    def get_source_info(
        self, avoid_clipboard_access: bool = True
    ) -> Optional[ProcessInfo]:
        """杂鱼♡～获取源信息，并把它从字典转成ProcessInfo喵～"""
        try:
            source_dict = StaticSourceTracker.get_source_info(avoid_clipboard_access)
            return self._convert_dict_to_process_info(source_dict)
        except Exception as e:
            self.logger.error(f"获取源信息时出错: {e}", exc_info=True)
            return None

    def get_status(self) -> Dict[str, Any]:
        """杂鱼♡～获取底层追踪器的状态喵～"""
        return StaticSourceTracker.get_focus_status()

    def cleanup(self):
        """杂鱼♡～清理底层的静态追踪器喵～"""
        self.logger.info("清理源追踪器...")
        StaticSourceTracker.cleanup_focus_tracking()

    def _convert_dict_to_process_info(
        self, source_info: Optional[Dict[str, Any]]
    ) -> Optional[ProcessInfo]:
        """杂鱼♡～将dict格式的source_info转换为ProcessInfo实例喵～"""
        if not source_info or not isinstance(source_info, dict):
            return None

        try:
            # 杂鱼♡～创建ProcessInfo实例，提供所有必需字段的默认值喵～
            return ProcessInfo(
                process_name=source_info.get("process_name", "Unknown"),
                process_path=source_info.get("process_path", ""),
                process_id=source_info.get("process_id", 0),
                window_title=source_info.get("window_title", ""),
                window_class=source_info.get("window_class", ""),
                detection_method=source_info.get("detection_method", "unknown"),
                confidence_level=source_info.get("confidence_level", "unknown"),
                is_system_process=source_info.get("is_system_process", False),
                is_screenshot_tool=source_info.get("is_screenshot_tool", False),
                timestamp=source_info.get("timestamp", time.time()),
            )
        except Exception as e:
            self.logger.error(f"杂鱼♡～转换source_info为ProcessInfo失败喵：{e}")
            return None
