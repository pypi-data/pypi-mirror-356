"""
讯飞虚拟人SDK for Python
支持虚拟人实时交互、文本驱动、语音交互等功能
"""

from .auth import AvatarAuth
from .avatar_client import AvatarClient
from .config import AvatarConfig
from .config_loader import ConfigLoader
from .exceptions import (AvatarAuthException, AvatarConnectionException,
                         AvatarSDKException)

__version__ = "1.0.0"
__author__ = "thoulee"

__all__ = [
    "AvatarClient",
    "AvatarAuth",
    "AvatarConfig",
    "ConfigLoader",
    "AvatarSDKException",
    "AvatarConnectionException",
    "AvatarAuthException"
]
