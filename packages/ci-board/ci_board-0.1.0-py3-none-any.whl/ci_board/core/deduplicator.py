# 杂鱼♡～这是本喵为主人写的内容去重器喵～
import hashlib
import json
import time
from typing import Any, Dict

from ..types import DIBData
from ..utils.logger import get_component_logger


class Deduplicator:
    """杂鱼♡～通过内容哈希来防止重复事件的喵～"""

    def __init__(
        self,
        cache_max_size: int = 10,
        image_dedup_window: float = 3.0,
        default_dedup_window: float = 1.0,
    ):
        self.logger = get_component_logger("core.deduplicator")
        self._last_content_hash: str = ""
        self._content_cache: Dict[str, float] = {}
        self._cache_max_size = cache_max_size
        self._image_dedup_window = image_dedup_window
        self._default_dedup_window = default_dedup_window

    def is_duplicate(self, content_type: str, content: Any) -> bool:
        """杂鱼♡～检查新内容是不是和最近的内容重复了喵～"""
        content_hash = self._calculate_content_hash(content_type, content)

        if content_hash == self._last_content_hash:
            self.logger.debug("内容哈希与上一个完全相同，跳过。")
            return True

        if content_hash in self._content_cache:
            last_time = self._content_cache[content_hash]
            threshold = (
                self._image_dedup_window
                if content_type == "image"
                else self._default_dedup_window
            )
            if time.time() - last_time < threshold:
                self.logger.debug(f"在 {threshold}s 的去重窗口内检测到重复内容，跳过。")
                return True

        self._last_content_hash = content_hash
        self._content_cache[content_hash] = time.time()
        self._cleanup_cache()
        return False

    def _cleanup_cache(self):
        """杂鱼♡～清理过期的缓存项喵～"""
        if len(self._content_cache) > self._cache_max_size:
            # 杂鱼♡～简单地按插入顺序（在Python 3.7+中）丢掉最旧的项喵～
            num_to_remove = len(self._content_cache) - self._cache_max_size
            for _ in range(num_to_remove):
                # 杂鱼♡～iter an d next 会获取第一个 (最老的) 键
                oldest_key = next(iter(self._content_cache))
                del self._content_cache[oldest_key]
            self.logger.debug(f"清理了 {num_to_remove} 个缓存项。")

    def _calculate_content_hash(self, content_type: str, content: Any) -> str:
        """杂鱼♡～为不同类型的内容计算哈希值喵～"""
        try:
            if content_type == "text":
                return hashlib.md5(content.encode("utf-8")).hexdigest()
            elif content_type == "image" and isinstance(content, DIBData):
                return self._calculate_image_fingerprint(content)
            elif content_type == "files" and isinstance(content, list):
                file_list = sorted(content)
                return hashlib.md5(json.dumps(file_list).encode("utf-8")).hexdigest()
            else:
                return hashlib.md5(str(content).encode("utf-8")).hexdigest()
        except Exception as e:
            self.logger.error(f"杂鱼♡～计算内容哈希失败喵：{e}")
            return str(time.time())  # 杂鱼♡～出错了就返回时间戳，避免错误地去重喵～

    def _calculate_image_fingerprint(self, image_data: DIBData) -> str:
        """杂鱼♡～为图片内容计算一个更可靠的指纹喵～"""
        # 杂鱼♡～用图片的元数据和部分像素数据来创建指纹喵～
        basic_features = (
            f"{image_data.width}x{image_data.height}_{image_data.bit_count}"
        )

        # 杂鱼♡～取头部、中部和尾部的数据样本来哈希喵～
        data = image_data.data
        if len(data) > 2048:
            sample = (
                data[:512]
                + data[len(data) // 2 - 256 : len(data) // 2 + 256]
                + data[-512:]
            )
        else:
            sample = data

        data_hash = hashlib.md5(sample).hexdigest()

        return f"img_{basic_features}_{data_hash}"
