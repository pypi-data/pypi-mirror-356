# 杂鱼♡～这是本喵为MessagePump写的包装器喵～
from typing import Any, Callable, Optional

from ci_board.utils import (
    get_component_logger,
    Win32API,
    MessagePump as StaticMessagePump,
)


class MessagePumpWrapper:
    """
    杂鱼♡～一个实例化的包装器，包住了静态的MessagePump喵～
    这让本喵可以把窗口句柄和回调函数之类的状态存在实例里，而不是全局的喵！
    """

    def __init__(self):
        self.logger = get_component_logger("core.message_pump_wrapper")
        self._hwnd: Optional[Any] = None
        self._clipboard_callback: Optional[Callable] = None

    def create_window(self, window_name: str = "NekoClipboardMonitor") -> bool:
        """杂鱼♡～创建用于监听的隐藏窗口喵～"""
        self.logger.info(f"正在创建名为 {window_name} 的隐藏窗口...")
        self._hwnd = StaticMessagePump.create_hidden_window(window_name)
        if not self._hwnd:
            self.logger.error("创建隐藏窗口失败了喵！")
            return False

        # 杂鱼♡～设置窗口回调，这样消息就能被处理了喵～
        StaticMessagePump.set_window_callback(self._hwnd, self._window_proc)
        return True

    def add_clipboard_listener(self, callback: Callable) -> bool:
        """杂鱼♡～为窗口添加剪贴板监听器喵～"""
        if not self._hwnd:
            self.logger.error("窗口还不存在，不能添加监听器喵！")
            return False

        self._clipboard_callback = callback
        self.logger.info("正在添加剪贴板格式监听器...")
        return StaticMessagePump.add_clipboard_listener(self._hwnd, self._window_proc)

    def pump_messages(self):
        """杂鱼♡～启动消息循环，开始处理Windows消息喵～"""
        if not self._hwnd:
            self.logger.error("窗口还不存在，不能启动消息泵喵！")
            return

        self.logger.info("消息泵启动，开始监听Windows消息...")
        # 杂鱼♡～pump_messages 在收到消息时返回 True，在收到 WM_QUIT 时返回 False
        # 所以循环条件应该是 while True 并检查返回值
        while StaticMessagePump.pump_messages(self._hwnd):
            pass  # 杂鱼♡～循环会一直持续，直到收到WM_QUIT喵～
        self.logger.info("消息泵已停止。")

    def stop_pump(self):
        """杂鱼♡～向消息循环发送退出消息喵～"""
        if self._hwnd:
            self.logger.info("正在发送退出消息到消息泵...")
            Win32API.user32.PostMessageW(self._hwnd, Win32API.WM_QUIT, 0, 0)

    def destroy_window(self):
        """杂鱼♡～销毁窗口和清理资源喵～"""
        if self._hwnd:
            self.logger.info("正在销毁窗口...")
            StaticMessagePump.remove_clipboard_listener(self._hwnd)
            StaticMessagePump.destroy_window(self._hwnd)
            self._hwnd = None

    def get_sequence_number(self) -> int:
        """杂鱼♡～获取当前的剪贴板序列号喵～"""
        return StaticMessagePump.get_clipboard_sequence_number()

    def _window_proc(self, msg: int, wParam: int, lParam: int) -> None:
        """杂鱼♡～这是一个实例方法，作为窗口过程的回调喵～"""
        if msg == Win32API.WM_CLIPBOARDUPDATE:
            self.logger.debug("收到了剪贴板更新消息！")
            if self._clipboard_callback:
                try:
                    self._clipboard_callback()
                except Exception as e:
                    self.logger.error(f"剪贴板回调函数执行出错喵: {e}", exc_info=True)
