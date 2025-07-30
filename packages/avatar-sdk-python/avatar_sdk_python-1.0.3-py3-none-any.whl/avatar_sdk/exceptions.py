"""
虚拟人SDK异常类定义
"""


class AvatarSDKException(Exception):
    """虚拟人SDK基础异常类"""

    def __init__(self, message: str, error_code: int = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class AvatarConnectionException(AvatarSDKException):
    """虚拟人连接异常"""
    pass


class AvatarAuthException(AvatarSDKException):
    """虚拟人认证异常"""
    pass


class AvatarMessageException(AvatarSDKException):
    """虚拟人消息异常"""
    pass
