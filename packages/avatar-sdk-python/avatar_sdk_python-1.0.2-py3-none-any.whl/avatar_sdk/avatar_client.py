"""
虚拟人客户端
"""

import json
import queue
import threading
import time
import uuid
from typing import Any, Callable, Dict, Optional

from ws4py.client.threadedclient import WebSocketBaseClient, WebSocketClient

from .auth import AvatarAuth
from .config import AvatarConfig
from .exceptions import (AvatarConnectionException, AvatarMessageException,
                         AvatarSDKException)


class AvatarClient(WebSocketClient, threading.Thread):
    """虚拟人客户端类"""

    def __init__(self, config: AvatarConfig):
        """
        初始化虚拟人客户端

        Args:
            config: 虚拟人配置对象
        """
        self.config = config

        # 构建认证URL
        self.auth_url = AvatarAuth.build_auth_url(
            config.base_url, 'GET', config.app_key, config.app_secret
        )

        # 初始化WebSocket客户端
        WebSocketBaseClient.__init__(
            self, self.auth_url, protocols=None, extensions=None,
            heartbeat_freq=None, ssl_options=None, headers=None,
            exclude_headers=None
        )
        threading.Thread.__init__(self)

        # 内部状态
        self._th = threading.Thread(target=super().run, name='WebSocketClient')
        self._th.daemon = True
        self.data_queue = queue.Queue(maxsize=100)
        self.status = True
        self.link_connected = False
        self.avatar_linked = False

        # 回调函数
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_stream_info: Optional[Callable] = None
        self.on_driver_status: Optional[Callable] = None
        self.on_interaction_result: Optional[Callable] = None

    def run(self):
        """启动虚拟人客户端"""
        try:
            self.connect()
            self._start_avatar()
            threading.Thread(target=self._send_message_loop,
                             daemon=True).start()

            while self.status and not self.terminated:
                self._th.join(timeout=0.1)

        except Exception as e:
            self.status = False
            if self.on_error:
                self.on_error(e)
            raise AvatarConnectionException(
                f"Failed to run avatar client: {str(e)}") from e

    def stop(self):
        """停止虚拟人客户端"""
        self.status = False
        self.close(code=1000)
        if self.on_disconnected:
            self.on_disconnected()

    def _send_message_loop(self):
        """消息发送循环"""
        while self.status:
            if self.link_connected:
                try:
                    if self.avatar_linked:
                        # 尝试获取消息
                        task = self.data_queue.get(block=True, timeout=5)
                        print(
                            f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} send msg: {task}')
                        self.send(task)
                except queue.Empty:
                    # 没有消息时发送ping
                    if self.status and self.avatar_linked:
                        self.send(self._get_ping_message())
                    else:
                        time.sleep(0.1)
                except AttributeError:
                    pass
            else:
                time.sleep(0.1)

    def send_text_driver(self, text: str, interactive_mode: Optional[int] = None) -> str:
        """
        发送文本驱动消息

        Args:
            text: 要驱动的文本内容
            interactive_mode: 交互模式，0追加，1打断，None使用配置默认值

        Returns:
            request_id: 请求ID
        """
        if not text or len(text) > 2000:
            raise AvatarMessageException(
                "Text content must be between 1 and 2000 characters")

        request_id = str(uuid.uuid4())

        if interactive_mode is None:
            interactive_mode = self.config.interactive_mode

        message = {
            "header": {
                "app_id": self.config.app_id,
                "request_id": request_id,
                "ctrl": "text_driver"
            },
            "parameter": {
                "tts": {
                    "vcn": self.config.vcn,
                    "speed": self.config.tts_speed,
                    "pitch": self.config.tts_pitch,
                    "volume": self.config.tts_volume
                },
                "avatar_dispatch": {
                    "interactive_mode": interactive_mode
                },
                "air": {
                    "air": self.config.air_enabled,
                    "add_nonsemantic": self.config.add_nonsemantic
                }
            },
            "payload": {
                "text": {
                    "content": text
                }
            }
        }

        try:
            self.data_queue.put_nowait(json.dumps(message))
            return request_id
        except queue.Full:
            raise AvatarMessageException("Message queue is full")

    def send_text_interact(self, text: str) -> str:
        """
        发送文本交互消息（带语义理解）

        Args:
            text: 要交互的文本内容

        Returns:
            request_id: 请求ID
        """
        if not text or len(text) > 2000:
            raise AvatarMessageException(
                "Text content must be between 1 and 2000 characters")

        request_id = str(uuid.uuid4())

        message = {
            "header": {
                "app_id": self.config.app_id,
                "request_id": request_id,
                "ctrl": "text_interact"
            },
            "parameter": {
                "tts": {
                    "vcn": self.config.vcn,
                    "speed": self.config.tts_speed,
                    "pitch": self.config.tts_pitch,
                    "volume": self.config.tts_volume
                },
                "air": {
                    "air": self.config.air_enabled,
                    "add_nonsemantic": self.config.add_nonsemantic
                }
            },
            "payload": {
                "text": {
                    "content": text
                }
            }
        }

        try:
            self.data_queue.put_nowait(json.dumps(message))
            return request_id
        except queue.Full:
            raise AvatarMessageException("Message queue is full")

    def _start_avatar(self):
        """启动虚拟人"""
        try:
            start_message = {
                "header": {
                    "app_id": self.config.app_id,
                    "request_id": str(uuid.uuid4()),
                    "ctrl": "start"
                },
                "parameter": {
                    "tts": {
                        "vcn": self.config.vcn
                    },
                    "avatar": {
                        "stream": {
                            "protocol": self.config.stream_protocol,
                            "fps": self.config.stream_fps,
                            "bitrate": self.config.stream_bitrate,
                            "alpha": self.config.stream_alpha
                        },
                        "avatar_id": self.config.avatar_id,
                        "width": self.config.width,
                        "height": self.config.height,
                        "scale": self.config.scale,
                        "move_h": self.config.move_h,
                        "move_v": self.config.move_v,
                        "audio_format": self.config.audio_format
                    }
                }
            }

            # 添加可选参数
            if self.config.mask_region:
                start_message["parameter"]["avatar"]["mask_region"] = self.config.mask_region

            if self.config.subtitle_enabled:
                start_message["parameter"]["subtitle"] = {
                    "subtitle": self.config.subtitle_enabled,
                    "font_color": self.config.font_color,
                    "font_size": self.config.font_size,
                    "font_name": self.config.font_name
                }

            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} send start request: {json.dumps(start_message)}")
            self.send(json.dumps(start_message))

        except Exception as e:
            raise AvatarConnectionException(
                f"Failed to start avatar: {str(e)}") from e

    def _get_ping_message(self) -> str:
        """获取ping消息"""
        ping_message = {
            "header": {
                "app_id": self.config.app_id,
                "request_id": str(uuid.uuid4()),
                "ctrl": "ping"
            }
        }
        return json.dumps(ping_message)

    def opened(self):
        """WebSocket连接打开回调"""
        self.link_connected = True
        if self.on_connected:
            self.on_connected()

    def closed(self, code, reason=None):
        """WebSocket连接关闭回调"""
        print(f'Connection closed, code: {code}, reason: {reason}')
        self.status = False
        if self.on_disconnected:
            self.on_disconnected(code, reason)

    def received_message(self, message):
        """接收消息回调"""
        try:
            data = json.loads(str(message))

            # 错误处理
            if data['header']['code'] != 0:
                self.status = False
                error_msg = f"Received error message: {str(message)}"
                print(error_msg)
                if self.on_error:
                    self.on_error(AvatarMessageException(
                        error_msg, data['header']['code']))
                return

            # 处理不同类型的响应
            self._handle_avatar_response(data)
            self._handle_nlp_response(data)

        except json.JSONDecodeError as e:
            if self.on_error:
                self.on_error(AvatarMessageException(
                    f"Failed to parse message: {str(e)}"))
        except Exception as e:
            if self.on_error:
                self.on_error(AvatarSDKException(
                    f"Error processing message: {str(e)}"))

    def _handle_avatar_response(self, data: Dict[str, Any]):
        """处理虚拟人响应"""
        if 'avatar' not in data.get('payload', {}):
            return

        avatar_data = data['payload']['avatar']
        event_type = avatar_data.get('event_type', '')

        if event_type == 'stream_info':
            self.avatar_linked = True
            stream_url = avatar_data.get('stream_url', '')
            print(f'Avatar connected: {str(data)}')
            print(f'Stream URL: {stream_url}')

            if self.on_stream_info:
                self.on_stream_info(
                    stream_url, avatar_data.get('stream_extend', {}))

        elif event_type == 'driver_status':
            if self.on_driver_status:
                self.on_driver_status(avatar_data)

        elif event_type == 'pong':
            # Ping-pong响应，无需特殊处理
            pass

        elif event_type == 'stop' and avatar_data.get('error_code') == 0:
            # 正常停止，继续运行
            pass

    def _handle_nlp_response(self, data: Dict[str, Any]):
        """处理NLP响应"""
        if 'nlp' not in data.get('payload', {}):
            return

        nlp_data = data['payload']['nlp']

        if self.on_interaction_result:
            self.on_interaction_result(nlp_data)

    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.link_connected and self.avatar_linked

    def get_status(self) -> Dict[str, Any]:
        """获取状态信息"""
        return {
            "status": self.status,
            "link_connected": self.link_connected,
            "avatar_linked": self.avatar_linked,
            "terminated": self.terminated,
            "queue_size": self.data_queue.qsize()
        }
