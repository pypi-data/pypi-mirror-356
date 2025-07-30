# 讯飞虚拟人 Python SDK

这是一个基于讯飞虚拟人实时交互API的Python SDK，提供了简单易用的接口来实现虚拟人交互功能。

## 功能特性

- ✅ 虚拟人实时连接管理
- ✅ 文本驱动（TTS + 动作）
- ✅ 文本交互（带语义理解）
- ✅ 音频驱动支持
- ✅ 完整的事件回调机制
- ✅ 错误处理和异常管理
- ✅ 灵活的配置选项
- ✅ **安全的敏感配置管理**
- ✅ **基于python-dotenv的环境变量支持**

## 安装依赖

```bash
poetry install
```

## 快速开始

### 1. 环境配置（重要）

**首次使用前，请先配置环境变量：**

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件，填入您的真实配置
# 在讯飞虚拟人交互平台申请相关参数
```

**`.env` 文件示例：**
```bash
# 应用基础信息（必填）
APP_ID=your_app_id
APP_KEY=your_app_key
APP_SECRET=your_app_secret
AVATAR_ID=your_avatar_id

# 可选配置
VCN=x4_xiaozhong
STREAM_PROTOCOL=webrtc
WIDTH=720
HEIGHT=1280
# ... 更多配置请参考 .env.example
```

### 2. 基础使用

```python
from avatar_sdk import AvatarClient, ConfigLoader

# 从环境变量加载配置（推荐方式）
config = ConfigLoader.load_from_env()

# 创建客户端
client = AvatarClient(config)
```

### 3. 设置回调并启动

```python
# 设置回调函数
def on_connected():
    print("虚拟人连接成功")

def on_stream_info(stream_url, stream_extend):
    print(f"流地址: {stream_url}")

client.on_connected = on_connected
client.on_stream_info = on_stream_info

# 启动客户端
client.start()

# 发送文本驱动
client.send_text_driver("你好，欢迎使用虚拟人!")
```

## 配置管理

### ConfigLoader 配置加载器

SDK提供了安全的配置加载器，支持从环境变量和.env文件加载配置：

```python
from avatar_sdk import ConfigLoader

# 方式1: 自动查找.env文件
config = ConfigLoader.load_from_env()

# 方式2: 指定.env文件路径
config = ConfigLoader.load_from_env(".env.production")

# 方式3: 静默模式（不输出日志）
config = ConfigLoader.load_from_env(silent=True)

# 配置验证
if ConfigLoader.validate_config(config):
    print("配置有效")
```

### 安全特性

1. **敏感信息脱敏**：日志中自动隐藏API密钥
2. **配置验证**：自动验证配置参数的有效性
3. **错误提示**：详细的错误信息和修复建议
4. **模板生成**：自动生成配置模板文件

```python
# 获取安全的配置字典（敏感信息已脱敏）
safe_config = ConfigLoader.get_safe_config_dict(config)

# 创建配置模板
ConfigLoader.create_env_template("my.env.example")
```

## 详细文档

### AvatarConfig 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `app_id` | str | - | 应用ID（必填） |
| `app_key` | str | - | 应用Key（必填） |
| `app_secret` | str | - | 应用Secret（必填） |
| `avatar_id` | str | - | 虚拟人形象ID（必填） |
| `vcn` | str | "x4_xiaozhong" | 发音人 |
| `base_url` | str | - | 连接地址 |
| `stream_protocol` | str | "webrtc" | 推流协议 |
| `stream_fps` | int | 25 | 推流帧率 |
| `stream_bitrate` | int | 2000 | 推流码率(kb) |
| `width` | int | 720 | 分辨率宽度 |
| `height` | int | 1280 | 分辨率高度 |
| `tts_speed` | int | 50 | 语音速度(0-100) |
| `tts_pitch` | int | 50 | 语音音调(0-100) |
| `tts_volume` | int | 50 | 语音音量(0-100) |
| `interactive_mode` | int | 0 | 交互模式(0追加/1打断) |

### 环境变量配置

支持的环境变量：

**必需配置：**
- `APP_ID`: 应用ID
- `APP_KEY`: 应用密钥
- `APP_SECRET`: 应用秘钥
- `AVATAR_ID`: 虚拟人形象ID

**推流配置：**
- `STREAM_PROTOCOL`: 推流协议（webrtc/rtmp/flv/xrtc）
- `WIDTH`/`HEIGHT`: 分辨率
- `STREAM_BITRATE`: 码率

**TTS配置：**
- `TTS_SPEED`/`TTS_PITCH`/`TTS_VOLUME`: 语音参数

**高级配置：**
- `AIR_ENABLED`: 自动动作
- `SUBTITLE_ENABLED`: 字幕
- `FONT_COLOR`/`FONT_SIZE`: 字体样式

### AvatarClient 主要方法

#### `send_text_driver(text: str, interactive_mode: int = None) -> str`
发送文本驱动消息

#### `send_text_interact(text: str) -> str`
发送文本交互消息（带语义理解）

#### `is_connected() -> bool`
检查是否已连接

#### `get_status() -> Dict[str, Any]`
获取状态信息

### 事件回调

| 回调函数 | 参数 | 说明 |
|----------|------|------|
| `on_connected` | - | 连接成功时触发 |
| `on_disconnected` | code, reason | 连接断开时触发 |
| `on_error` | error | 发生错误时触发 |
| `on_stream_info` | stream_url, stream_extend | 收到流信息时触发 |
| `on_driver_status` | avatar_data | 驱动状态变化时触发 |
| `on_interaction_result` | nlp_data | 收到交互结果时触发 |

## 示例文件

| 文件 | 说明 |
|------|------|
| `example.py` | 基础使用示例 |
| `advanced_example.py` | 高级功能演示 |

### 🛡️ 配置验证

```python
# 自动验证配置
if not ConfigLoader.validate_config(config):
    raise ValueError("配置验证失败")
```

## 异常处理

SDK提供了完整的异常处理机制：

- `AvatarSDKException`: SDK基础异常
- `AvatarConnectionException`: 连接异常
- `AvatarAuthException`: 认证异常  
- `AvatarMessageException`: 消息异常

```python
from avatar_sdk.exceptions import AvatarSDKException, AvatarConnectionException

try:
    config = ConfigLoader.load_from_env()
    client = AvatarClient(config)
    client.send_text_driver("测试消息")
except ValueError as e:
    print(f"配置错误: {e}")
except AvatarConnectionException as e:
    print(f"连接异常: {e}")
except AvatarSDKException as e:
    print(f"SDK异常: {e}")
```

## 注意事项

1. **API权限**: 请确保已在讯飞虚拟人平台申请相关权限和资源
2. **文本长度**: 文本内容长度限制为2000字符以内
3. **错误处理**: 建议设置合适的错误处理回调
4. **网络异常**: 长时间运行时注意处理网络异常和重连机制
5. **配置安全**: 妥善保管API密钥，定期进行安全检查

## 版本历史

- v1.0.0: 初始版本，支持基础虚拟人交互功能和安全配置管理

## 许可证

本项目基于MIT许可证开源。
