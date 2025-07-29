# 杂鱼♡～这是本喵为主人写的异步处理器执行器喵～
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional

from ci_board.utils import get_component_logger


class AsyncExecutor:
    """杂鱼♡～负责异步执行处理器，并管理线程池的喵～"""

    def __init__(self, max_workers: int = 4, handler_timeout: float = 30.0):
        self._max_workers = max_workers
        self._handler_timeout = handler_timeout
        self._executor: Optional[ThreadPoolExecutor] = None
        self._task_queue = queue.Queue()
        self._executor_thread: Optional[threading.Thread] = None
        self._executor_stop_event = threading.Event()
        self.logger = get_component_logger("core.executor")
        self._stats = {
            "tasks_submitted": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "tasks_timeout": 0,
            "active_tasks": 0,
        }

    def start(self):
        """杂鱼♡～启动执行器和线程池喵～"""
        self.logger.info(
            f"杂鱼♡～初始化异步执行器，最大工作线程：{self._max_workers}，超时：{self._handler_timeout}s喵～"
        )
        self._executor = ThreadPoolExecutor(
            max_workers=self._max_workers, thread_name_prefix="NekoHandler"
        )
        self._executor_stop_event.clear()
        self._executor_thread = threading.Thread(target=self._run, daemon=True)
        self._executor_thread.start()

    def stop(self):
        """杂鱼♡～关闭执行器喵～"""
        if not self._executor:
            return

        self.logger.info("杂鱼♡～正在关闭异步执行器喵～")
        self._executor_stop_event.set()
        # 杂鱼♡～放入一个None来唤醒等待中的队列，让循环可以结束喵～
        self._task_queue.put(None)

        if self._executor_thread and self._executor_thread.is_alive():
            self._executor_thread.join(timeout=2.0)

        self._executor.shutdown(wait=False)
        self._executor = None
        self.logger.info("杂鱼♡～异步执行器已关闭喵～")

    def submit(self, handler_method: Callable, args: tuple):
        """杂鱼♡～提交一个新任务到队列里喵～"""
        self._task_queue.put((handler_method, args))

    def get_stats(self) -> Dict[str, Any]:
        """杂鱼♡～获取执行器统计信息喵～"""
        return {
            "max_workers": self._max_workers,
            "handler_timeout": self._handler_timeout,
            "is_running": self._executor is not None,
            "queue_size": self._task_queue.qsize(),
            **self._stats,
        }

    def _run(self):
        """杂鱼♡～异步执行器的主循环喵～"""
        futures: Dict[Any, tuple] = {}

        while not self._executor_stop_event.is_set():
            try:
                # 杂鱼♡～处理新任务喵～
                self._process_new_tasks(futures)
                # 杂鱼♡～检查并清理已完成的任务喵～
                self._check_and_cleanup_completed_tasks(futures)
                time.sleep(0.01)  # 杂鱼♡～适当休息一下喵～
            except Exception as e:
                self.logger.error(f"杂鱼♡～异步执行器循环出错了喵：{e}", exc_info=True)
                time.sleep(0.1)

        self._cleanup_remaining_futures(futures)

    def _process_new_tasks(self, futures: dict):
        """杂鱼♡～从队列里获取新任务并提交到线程池喵～"""
        try:
            task = self._task_queue.get(timeout=0.1)
            if task is None:  # 杂鱼♡～这是停止信号喵～
                self._executor_stop_event.set()
                return

            handler_method, args = task
            future = self._executor.submit(handler_method, *args)
            futures[future] = (handler_method.__qualname__, time.time())
            self._stats["tasks_submitted"] += 1
            self._stats["active_tasks"] += 1
        except queue.Empty:
            pass  # 杂鱼♡～队列是空的，没关系喵～

    def _check_and_cleanup_completed_tasks(self, futures: dict):
        """杂鱼♡～检查任务是否完成或超时喵～"""
        completed = []
        for future, (handler_name, start_time) in futures.items():
            if future.done():
                completed.append(future)
                try:
                    future.result()  # 杂鱼♡～获取结果可以暴露执行期间的异常喵～
                    self._stats["tasks_completed"] += 1
                except Exception as e:
                    self.logger.error(
                        f"处理器 {handler_name} 执行失败喵: {e}", exc_info=True
                    )
                    self._stats["tasks_failed"] += 1
            elif time.time() - start_time > self._handler_timeout:
                completed.append(future)
                future.cancel()
                self.logger.warning(f"处理器 {handler_name} 超时了喵！")
                self._stats["tasks_timeout"] += 1

        for future in completed:
            del futures[future]
            self._stats["active_tasks"] -= 1

    def _cleanup_remaining_futures(self, futures: dict):
        """杂鱼♡～清理循环结束时还没完成的任务喵～"""
        self.logger.info(f"清理 {len(futures)} 个剩余任务喵...")
        for future in futures.keys():
            future.cancel()
