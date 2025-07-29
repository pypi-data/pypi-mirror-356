# 杂鱼♡～本喵的图片处理器喵～
import ctypes
import datetime
from typing import Callable, List, Optional

from ..interfaces.callback_interface import BaseClipboardHandler
from ..types import BMPData, DIBData, ProcessInfo
from ..utils.win32_api import ClipboardFormat, Win32API, Win32Structures
from ci_board.utils import get_component_logger

# 杂鱼♡～获取组件专用logger喵～
logger = get_component_logger("handlers.image_handler")

# 杂鱼♡～Windows GDI常量喵～
DIB_RGB_COLORS = 0
BI_RGB = 0


class ImageHandler(BaseClipboardHandler[DIBData]):
    """杂鱼♡～专门处理图片的处理器喵～"""

    def __init__(
        self,
        callback: Optional[Callable[[BMPData, Optional[ProcessInfo]], None]] = None,
    ):
        """
        杂鱼♡～初始化图片处理器喵～

        Args:
            callback: 处理BMP图片的回调函数, 接收 (bmp_data, source_info)
        """
        super().__init__(callback)

    def get_interested_formats(self) -> List[int]:
        """杂鱼♡～本喵对两种DIB格式都感兴趣喵～"""
        return [ClipboardFormat.CF_DIBV5.value, ClipboardFormat.CF_DIB.value]

    def process_data(self, format_id: int, handle: int, source_info: Optional[ProcessInfo]) -> None:
        """杂鱼♡～处理DIB的原始句柄，把它变成BMP喵～"""
        if not self._enabled:
            return

        dib_data = self._read_dib_from_handle(handle)
        if not dib_data:
            return

        bmp_data = self._convert_dib_to_bmp(dib_data)
        if not bmp_data or not bmp_data.success:
            self.logger.warning("DIB转BMP失败，跳过回调。")
            return

        if self._callback:
            try:
                import inspect
                sig = inspect.signature(self._callback)
                if len(sig.parameters) >= 2:
                    self._callback(bmp_data, source_info if self._include_source_info else None)
                else:
                    self._callback(bmp_data)
            except (ValueError, TypeError):
                self._callback(bmp_data)
        else:
            self._default_handle(bmp_data, source_info)

    def _read_dib_from_handle(self, handle: int) -> Optional[DIBData]:
        """杂鱼♡～从句柄读取DIB数据喵～"""
        try:
            ptr = Win32API.kernel32.GlobalLock(handle)
            if not ptr:
                return None
            try:
                header = Win32Structures.BITMAPINFOHEADER.from_address(ptr)
                if header.biWidth <= 0 or abs(header.biHeight) <= 0:
                    return None

                data_size = Win32API.kernel32.GlobalSize(handle)
                raw_data = ctypes.string_at(ptr, data_size)
                if not raw_data:
                    return None

                return DIBData(
                    width=header.biWidth,
                    height=abs(header.biHeight),
                    bit_count=header.biBitCount,
                    compression=header.biCompression,
                    data=raw_data,
                    header=header,
                )
            finally:
                Win32API.kernel32.GlobalUnlock(handle)
        except Exception as e:
            self.logger.error(f"读取DIB句柄失败喵: {e}", exc_info=True)
            return None

    def _convert_dib_to_bmp(self, dib_data: DIBData) -> Optional[BMPData]:
        """杂鱼♡～将DIB数据转换为BMP格式数据喵～"""
        try:
            dib_bytes = dib_data.data
            header_size = dib_data.header.biSize
            bit_count = dib_data.bit_count
            compression = dib_data.compression

            pixel_offset = 14 + header_size
            if bit_count <= 8:
                clr_used = dib_data.header.biClrUsed
                color_table_size = (1 << bit_count) * 4 if clr_used == 0 else clr_used * 4
                pixel_offset += color_table_size
            elif compression == 3:  # BI_BITFIELDS
                pixel_offset += 12

            file_size = 14 + len(dib_bytes)
            bmp_bytes = bytearray()
            bmp_bytes.extend(b"BM")
            bmp_bytes.extend(file_size.to_bytes(4, "little"))
            bmp_bytes.extend(b"\x00\x00\x00\x00")
            bmp_bytes.extend(pixel_offset.to_bytes(4, "little"))
            bmp_bytes.extend(dib_bytes)

            return BMPData(
                success=True, data=bytes(bmp_bytes), width=dib_data.width,
                height=dib_data.height, bit_count=dib_data.bit_count,
                timestamp=str(datetime.datetime.now())
            )
        except Exception as e:
            self.logger.error(f"DIB转BMP时出错: {e}", exc_info=True)
            return None

    def _default_handle(
        self, data: BMPData, source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认的图片处理方法喵～"""
        self.logger.info("杂鱼♡～检测到图片变化喵～")

        if data.success:
            self.logger.info(f"杂鱼♡～BMP格式图片：{data.width}x{data.height}喵～")
            self.logger.info(f"杂鱼♡～BMP文件大小：{len(data.data)}字节喵～")
        else:
            self.logger.warning("杂鱼♡～收到了失败的BMPData喵～")
            return

        if source_info and self._include_source_info:
            self.logger.info(f"  源应用程序：{source_info.process_name}")
            if source_info.process_path:
                self.logger.debug(f"  程序路径：{source_info.process_path}")
        self.logger.info("-" * 50)
