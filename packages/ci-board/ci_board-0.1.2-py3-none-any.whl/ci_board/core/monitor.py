# 杂鱼♡～本喵的核心剪贴板监控器喵～
import threading
import time
from typing import Callable, Dict, List, Literal, Optional, Union

from ci_board.interfaces import BaseClipboardHandler
from ci_board.types import ProcessInfo
from ci_board.utils import ClipboardReader, get_component_logger
from ci_board.handlers import FileHandler, ImageHandler, TextHandler

# 杂鱼♡～导入核心组件喵～
from ci_board.core.executor import AsyncExecutor
from ci_board.core.message_pump_wrapper import MessagePumpWrapper
from ci_board.core.source_tracker_wrapper import SourceTrackerWrapper


class ClipboardMonitor:
    """
    杂鱼♡～本喵重构后的高扩展性剪贴板监控器喵～
    现在本喵是纯粹的指挥官，把具体工作都交给手下去做了喵！
    """

    def __init__(
        self,
        async_processing: bool = True,
        max_workers: int = 4,
        handler_timeout: float = 30.0,
        enable_source_tracking: bool = True,
    ):
        self.logger = get_component_logger("monitor")
        self._handlers: Dict[str, List[BaseClipboardHandler]] = {
            "text": [],
            "image": [],
            "files": [],
        }
        self._is_running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # 杂鱼♡～把工作交给这些专业的组件喵～
        self._enable_source_tracking = enable_source_tracking
        self._async_processing = async_processing

        # 杂鱼♡～实例化各个组件喵～
        self._pump = MessagePumpWrapper()
        self._reader = ClipboardReader()
        if self._enable_source_tracking:
            self._source_tracker = SourceTrackerWrapper()
        else:
            self._source_tracker = None
        if self._async_processing:
            self._executor = AsyncExecutor(
                max_workers=max_workers, handler_timeout=handler_timeout
            )
        else:
            self._executor = None

        self._last_sequence_number = 0

    def add_handler(
        self,
        content_type: Literal["text", "image", "files"],
        handler: Union[BaseClipboardHandler, Callable],
    ) -> BaseClipboardHandler:
        """杂鱼♡～添加处理器喵～"""
        if content_type not in self._handlers:
            raise ValueError(f"杂鱼♡～不支持的内容类型：{content_type}")

        if not isinstance(handler, BaseClipboardHandler):
            if callable(handler):
                handler = self._create_handler_from_callback(content_type, handler)
            else:
                raise TypeError(
                    "杂鱼♡～处理器必须是BaseClipboardHandler的子类或者一个可调用对象喵～"
                )

        self._handlers[content_type].append(handler)
        self.logger.info(
            f"成功添加 {type(handler).__name__} 到 {content_type} 处理器列表。"
        )
        return handler

    def _create_handler_from_callback(
        self, content_type: str, callback: Callable
    ) -> BaseClipboardHandler:
        """杂鱼♡～根据回调函数创建对应的处理器喵～"""
        if content_type == "text":
            return TextHandler(callback)
        if content_type == "image":
            return ImageHandler(callback)
        if content_type == "files":
            return FileHandler(callback)
        raise ValueError(f"杂鱼♡～无法为类型 {content_type} 创建处理器喵～")

    def start(self) -> bool:
        """杂鱼♡～启动监控器喵～"""
        if self._is_running:
            self.logger.warning("监控器已经在运行了，杂鱼别重复启动喵！")
            return False

        self._stop_event.clear()

        # 杂鱼♡～只启动执行器，追踪器和消息泵的初始化都放到监控线程里喵～
        if self._executor:
            self._executor.start()

        # 杂鱼♡～创建监听线程喵～
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=False)
        self._monitor_thread.start()

        # 杂鱼♡～等待窗口创建完成（这里简化了，实际需要事件同步）
        time.sleep(1)

        self._is_running = True
        self.logger.info(
            f"剪贴板监控已启动 (异步: {self._async_processing}, 源追踪: {self._enable_source_tracking})"
        )
        return True

    def stop(self) -> None:
        """杂鱼♡～停止监控器喵～"""
        if not self._is_running:
            return

        self.logger.info("正在停止监控器...")
        self._stop_event.set()

        # 杂鱼♡～停止组件喵～
        if self._executor:
            self._executor.stop()
        if self._source_tracker:
            self._source_tracker.cleanup()

        self._pump.stop_pump()  # 杂鱼♡～这会终止消息循环喵～

        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=3.0)
            if self._monitor_thread.is_alive():
                self.logger.warning("监控线程未能正常退出喵！")

        self._is_running = False
        self.logger.info("剪贴板监控已停止。")

    def wait(self) -> None:
        """杂鱼♡～等待监控器结束喵～"""
        if not self._is_running or not self._monitor_thread:
            return
        try:
            # 杂鱼♡～用带超时的循环等待，这样主线程才能响应Ctrl+C喵～
            while self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=0.25)
        except KeyboardInterrupt:
            self.logger.info("被用户中断了喵～")
            self.stop()
            # 杂鱼♡～重新抛出异常，让程序可以正常退出喵～
            raise

    def _monitor_loop(self) -> None:
        """杂鱼♡～监控循环，现在负责初始化和运行消息泵和追踪器喵～"""
        # 杂鱼♡～在这里初始化追踪器，确保和消息循环在同一个线程喵！～
        if self._source_tracker:
            self._source_tracker.initialize()

        if not self._pump.create_window():
            return

        if not self._pump.add_clipboard_listener(callback=self._on_clipboard_update):
            self.logger.error("添加剪贴板监听器失败！")
            self._pump.destroy_window()
            return

        self.logger.info("开始处理Windows消息...")
        self._pump.pump_messages()

        # 杂鱼♡～清理窗口资源喵～
        self._pump.destroy_window()
        self.logger.info("监控循环结束。")

    def _on_clipboard_update(self) -> None:
        """杂鱼♡～处理剪贴板更新的核心逻辑喵～"""
        current_seq = self._pump.get_sequence_number()
        if current_seq == self._last_sequence_number:
            return
        self._last_sequence_number = current_seq

        time.sleep(0.05)

        source_info: Optional[ProcessInfo] = None
        if self._source_tracker:
            source_info = self._source_tracker.get_source_info(avoid_clipboard_access=False)

        available_formats = self._reader.get_available_formats()
        if not available_formats:
            return

        self.logger.debug(f"剪贴板上有这些格式喵: {available_formats}")

        # 杂鱼♡～为每个可用的格式找到对它感兴趣的处理器喵～
        for format_id in available_formats:
            # 杂鱼♡～先不获取句柄，只检查有没有处理器对它感兴趣
            interested_handlers = []
            for handler_list in self._handlers.values():
                for handler in handler_list:
                    if format_id in handler.get_interested_formats():
                        interested_handlers.append(handler)

            # 杂鱼♡～如果找到了，就获取句柄并分发任务喵～
            if interested_handlers:
                handle = self._reader.get_handle_for_format(format_id)
                if not handle:
                    self.logger.warning(f"无法获取格式 {format_id} 的句柄喵！")
                    continue

                # 杂鱼♡～只处理一次，避免重复喵～
                self.logger.info(f"为格式 {format_id} 找到了 {len(interested_handlers)} 个处理器，开始处理...")
                for handler in interested_handlers:
                    self._dispatch_to_handler(handler, format_id, handle, source_info)

                # 杂鱼♡～处理完一种格式后就跳出，避免同一个剪贴板事件被不同类型的处理器重复处理
                # （比如一个事件同时有文本和图片格式）
                # 哼，这里可以根据杂鱼主人的需求调整策略喵～
                break

    def _dispatch_to_handler(self, handler: BaseClipboardHandler, format_id: int, handle: int, source_info: Optional[ProcessInfo]):
        """杂鱼♡～把原始数据句柄分发给单个处理器喵～"""
        if self._executor:
            self.logger.debug(f"异步提交任务给 {type(handler).__name__}...")
            # 注意：这里的 executor 需要能够接受这些参数
            self._executor.submit(handler.process_data, (format_id, handle, source_info))
        else:
            self.logger.debug(f"同步执行处理器 {type(handler).__name__}...")
            try:
                handler.process_data(format_id, handle, source_info)
            except Exception as e:
                self.logger.error(f"同步执行处理器失败喵: {e}", exc_info=True)

    def get_status(self) -> dict:
        """杂鱼♡～获取监控器状态喵～"""
        status = {
            "is_running": self._is_running,
            "async_processing": self._async_processing,
            "source_tracking_enabled": self._enable_source_tracking,
            "handlers_count": {k: len(v) for k, v in self._handlers.items()},
            "last_sequence_number": self._last_sequence_number,
        }
        if self._executor:
            status["executor_stats"] = self._executor.get_stats()
        if self._source_tracker:
            status["source_tracker_status"] = self._source_tracker.get_status()
        return status
