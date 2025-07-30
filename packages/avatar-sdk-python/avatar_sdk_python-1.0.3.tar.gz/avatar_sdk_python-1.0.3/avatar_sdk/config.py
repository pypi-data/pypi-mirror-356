"""
虚拟人SDK配置类
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AvatarConfig:
    """虚拟人配置类"""

    # 基础认证信息
    app_id: str
    app_key: str
    app_secret: str

    # 虚拟人形象配置
    avatar_id: str
    vcn: str = "x4_xiaozhong"  # 默认发音人

    # WebSocket连接配置
    base_url: str = "wss://avatar.cn-huadong-1.xf-yun.com/v1/interact"

    # 推流配置
    stream_protocol: str = "webrtc"  # rtmp, xrtc, webrtc, flv
    stream_fps: int = 25
    stream_bitrate: int = 2000
    stream_alpha: int = 0
    width: int = 720
    height: int = 1280

    # TTS配置
    tts_speed: int = 50
    tts_pitch: int = 50
    tts_volume: int = 50

    # 动作配置
    air_enabled: int = 0  # 自动动作
    add_nonsemantic: int = 0  # 无指向性动作

    # 字幕配置
    subtitle_enabled: int = 0
    font_color: str = "#FFFFFF"
    font_size: int = 1
    font_name: str = "mainTitle"

    # 其他配置
    mask_region: Optional[str] = None
    scale: float = 1.0
    move_h: int = 0
    move_v: int = 0
    audio_format: int = 1

    # 交互模式：0追加，1打断
    interactive_mode: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "avatar_id": self.avatar_id,
            "vcn": self.vcn,
            "base_url": self.base_url,
            "stream_protocol": self.stream_protocol,
            "stream_fps": self.stream_fps,
            "stream_bitrate": self.stream_bitrate,
            "stream_alpha": self.stream_alpha,
            "width": self.width,
            "height": self.height,
            "tts_speed": self.tts_speed,
            "tts_pitch": self.tts_pitch,
            "tts_volume": self.tts_volume,
            "air_enabled": self.air_enabled,
            "add_nonsemantic": self.add_nonsemantic,
            "subtitle_enabled": self.subtitle_enabled,
            "font_color": self.font_color,
            "font_size": self.font_size,
            "font_name": self.font_name,
            "mask_region": self.mask_region,
            "scale": self.scale,
            "move_h": self.move_h,
            "move_v": self.move_v,
            "audio_format": self.audio_format,
            "interactive_mode": self.interactive_mode
        }
