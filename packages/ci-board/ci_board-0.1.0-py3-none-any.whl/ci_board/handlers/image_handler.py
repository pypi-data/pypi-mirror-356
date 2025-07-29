# 杂鱼♡～本喵的图片处理器喵～
import datetime
from typing import Callable, Optional

from ..interfaces.callback_interface import BaseClipboardHandler
from ..types import BMPData, DIBData, ProcessInfo
from ..utils.logger import get_component_logger

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

    def handle(self, data: DIBData, source_info: Optional[ProcessInfo] = None) -> None:
        """杂鱼♡～重写handle方法，将DIB数据转换为BMP格式喵～"""
        if not self._enabled or not self.is_valid(data):
            return

        try:
            bmp_data = self._convert_dib_to_bmp(data)
            if not bmp_data or not bmp_data.success:
                self.logger.warning("DIB转BMP失败，跳过回调。")
                return
        except Exception as e:
            self.logger.error(f"杂鱼♡～DIB转换过程出错喵：{e}")
            return

        # 杂鱼♡～直接调用回调或默认处理，不再调用super().handle喵！～
        if self._callback:
            # 杂鱼♡～本喵会帮你检查回调函数需不需要源信息喵～
            import inspect

            try:
                sig = inspect.signature(self._callback)
                # 杂鱼♡～处理BMP数据和源信息喵～
                if len(sig.parameters) >= 2:
                    self._callback(
                        bmp_data, source_info if self._include_source_info else None
                    )
                else:
                    self._callback(bmp_data)
            except (ValueError, TypeError):
                self._callback(bmp_data)  # 杂鱼♡～出错了就默认只传数据喵～
        else:
            self._default_handle(bmp_data, source_info)

    def _convert_dib_to_bmp(self, dib_data: DIBData) -> Optional[BMPData]:
        """杂鱼♡～将DIB数据转换为BMP格式数据喵～"""
        try:
            bmp_bytes = self._create_bmp_bytes_from_dib(dib_data)
            if bmp_bytes:
                return BMPData(
                    success=True,
                    data=bmp_bytes,
                    width=dib_data.width,
                    height=dib_data.height,
                    bit_count=dib_data.bit_count,
                    timestamp=str(datetime.datetime.now()),
                )
            else:
                self.logger.warning("杂鱼♡～创建BMP字节失败喵～")
                return None
        except Exception as e:
            self.logger.error(f"DIB转BMP时出错: {e}", exc_info=True)
            return None

    def is_valid(self, data: Optional[DIBData] = None) -> bool:
        """杂鱼♡～检查DIB数据是否有效喵～"""
        if not isinstance(data, DIBData):
            return False

        if data.width <= 0 or data.height <= 0:
            self.logger.warning(f"无效的图片尺寸: {data.width}x{data.height}")
            return False

        if not data.data or len(data.data) < 40:  # BITMAPINFOHEADER至少40字节
            self.logger.warning("DIB数据为空或过小")
            return False

        return True

    def _default_handle(
        self, data: BMPData, source_info: Optional[ProcessInfo] = None
    ) -> None:
        """杂鱼♡～默认的图片处理方法喵～"""
        # 杂鱼♡～现在收到的已经是BMPData了，直接用就行了喵～
        self.logger.info("杂鱼♡～检测到图片变化喵～")

        if data.success:
            self.logger.info(f"杂鱼♡～BMP格式图片：{data.width}x{data.height}喵～")
            self.logger.info(f"杂鱼♡～BMP文件大小：{len(data.data)}字节喵～")
        else:
            # 理论上不会走到这里，因为handle里已经检查过了
            self.logger.warning("杂鱼♡～收到了失败的BMPData喵～")
            return

        # 杂鱼♡～显示源应用程序信息喵～
        if source_info and self._include_source_info:
            self.logger.info(f"  源应用程序：{source_info.process_name}")
            if source_info.process_path:
                self.logger.debug(f"  程序路径：{source_info.process_path}")
            if source_info.window_title:
                self.logger.debug(f"  窗口标题：{source_info.window_title}")

        self.logger.info("-" * 50)

    def _create_bmp_bytes_from_dib(self, dib_data: DIBData) -> Optional[bytes]:
        """
        杂鱼♡～根据DIB数据创建完整的BMP文件字节流喵～
        哼～再也不用去重新读剪贴板了，用传进来的数据就行了喵！
        """
        try:
            # 杂鱼♡～从DIB数据中获取信息喵～
            dib_bytes = dib_data.data
            bit_count = dib_data.bit_count
            compression = dib_data.compression
            header_size = 40  # 通常是BITMAPINFOHEADER的大小

            # 杂鱼♡～计算像素数据偏移喵～
            pixel_offset = 14 + header_size  # 文件头(14) + DIB头

            # 杂鱼♡～如果有调色板或位字段掩码，需要加上大小喵～
            if bit_count <= 8:
                # 杂鱼♡～调色板模式喵～
                # 杂鱼♡～从DIB数据中读取clr_used喵～
                if len(dib_bytes) >= 36:
                    clr_used = int.from_bytes(dib_bytes[32:36], "little")
                else:
                    clr_used = 0

                if clr_used > 0:
                    color_table_size = clr_used * 4
                else:
                    color_table_size = (1 << bit_count) * 4
                pixel_offset += color_table_size
            elif compression == 3:  # BI_BITFIELDS
                # 杂鱼♡～位字段掩码，通常是3个DWORD喵～
                pixel_offset += 12  # 3 * 4字节

            # 杂鱼♡～创建BMP文件头喵～
            file_header_size = 14
            file_size = file_header_size + len(dib_bytes)

            # 杂鱼♡～构建完整的BMP字节数据喵～
            bmp_bytes = bytearray()
            bmp_bytes.extend(b"BM")  # BMP签名
            bmp_bytes.extend(file_size.to_bytes(4, "little"))  # 文件大小
            bmp_bytes.extend(b"\x00\x00\x00\x00")  # 保留字段
            bmp_bytes.extend(pixel_offset.to_bytes(4, "little"))  # 像素数据偏移
            bmp_bytes.extend(dib_bytes)  # DIB数据

            self.logger.info(
                f"杂鱼♡～BMP转换成功：{dib_data.width}x{abs(dib_data.height)}，{bit_count}位，文件大小{len(bmp_bytes)}字节喵～"
            )
            return bytes(bmp_bytes)

        except Exception as e:
            self.logger.error(f"杂鱼♡～创建BMP字节数据失败喵：{e}", exc_info=True)
            return None
