"""
配置加载器
用于从环境变量加载配置，支持安全的敏感信息处理
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import find_dotenv, load_dotenv

from .config import AvatarConfig


class ConfigLoader:
    """配置加载器类"""

    # 必需的环境变量列表
    REQUIRED_VARS = ['APP_ID', 'APP_KEY', 'APP_SECRET', 'AVATAR_ID']

    # 敏感配置项（不会在日志中显示）
    SENSITIVE_KEYS = ['APP_KEY', 'APP_SECRET']

    @staticmethod
    def load_from_env(env_file: Optional[str] = None,
                      silent: bool = False) -> AvatarConfig:
        """
        从环境变量加载配置

        Args:
            env_file: .env文件路径，默认为None（自动查找）
            silent: 是否静默模式（不输出日志）

        Returns:
            AvatarConfig: 配置对象

        Raises:
            ValueError: 缺少必需的环境变量
            FileNotFoundError: 指定的.env文件不存在
        """
        # 设置日志
        logger = logging.getLogger(__name__)
        if not silent:
            logging.basicConfig(level=logging.INFO)

        # 加载环境变量
        if env_file:
            if Path(env_file).exists():
                load_dotenv(env_file)
                if not silent:
                    logger.info(f"✅ 从指定文件加载环境变量: {env_file}")
            else:
                raise FileNotFoundError(f"指定的.env文件不存在: {env_file}")
        else:
            # 自动查找.env文件
            found_env = find_dotenv()
            if found_env:
                load_dotenv(found_env)
                if not silent:
                    logger.info(f"✅ 自动发现并加载环境变量文件: {found_env}")
            else:
                if not silent:
                    logger.warning("⚠️ 未找到.env文件，将使用系统环境变量")

        # 验证必需的环境变量
        missing_vars = ConfigLoader._validate_required_vars()
        if missing_vars:
            error_msg = f"缺少必需的环境变量: {', '.join(missing_vars)}"
            if not silent:
                logger.error(f"❌ {error_msg}")
                logger.info("请检查以下项目:")
                logger.info("1. .env文件是否存在且包含所有必需配置")
                logger.info("2. 环境变量是否正确设置")
                logger.info("3. 参考 .env.example 文件进行配置")
            raise ValueError(error_msg)

        # 获取配置值
        config_values = ConfigLoader._extract_config_values()

        # 创建配置对象
        config = AvatarConfig(**config_values)

        # 验证配置
        if not ConfigLoader.validate_config(config):
            error_msg = "配置验证失败，请检查配置参数的有效性"
            if not silent:
                logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)

        if not silent:
            logger.info("✅ 配置加载并验证成功")
            ConfigLoader._log_config_summary(config, logger)

        return config

    @staticmethod
    def _validate_required_vars() -> List[str]:
        """验证必需的环境变量"""
        missing = []
        for var in ConfigLoader.REQUIRED_VARS:
            if not os.getenv(var):
                missing.append(var)
        return missing

    @staticmethod
    def _extract_config_values() -> Dict[str, Any]:
        """提取配置值"""
        return {
            # 必需参数
            'app_id': os.getenv('APP_ID'),
            'app_key': os.getenv('APP_KEY'),
            'app_secret': os.getenv('APP_SECRET'),
            'avatar_id': os.getenv('AVATAR_ID'),

            # 可选参数（带默认值）
            'vcn': os.getenv('VCN', 'x4_xiaozhong'),
            'base_url': os.getenv('BASE_URL', 'wss://avatar.cn-huadong-1.xf-yun.com/v1/interact'),

            # 推流配置
            'stream_protocol': os.getenv('STREAM_PROTOCOL', 'webrtc'),
            'stream_fps': int(os.getenv('STREAM_FPS', '25')),
            'stream_bitrate': int(os.getenv('STREAM_BITRATE', '2000')),
            'stream_alpha': int(os.getenv('STREAM_ALPHA', '0')),
            'width': int(os.getenv('WIDTH', '720')),
            'height': int(os.getenv('HEIGHT', '1280')),

            # TTS配置
            'tts_speed': int(os.getenv('TTS_SPEED', '50')),
            'tts_pitch': int(os.getenv('TTS_PITCH', '50')),
            'tts_volume': int(os.getenv('TTS_VOLUME', '50')),

            # 动作配置
            'air_enabled': int(os.getenv('AIR_ENABLED', '0')),
            'add_nonsemantic': int(os.getenv('ADD_NONSEMANTIC', '0')),

            # 字幕配置
            'subtitle_enabled': int(os.getenv('SUBTITLE_ENABLED', '0')),
            'font_color': os.getenv('FONT_COLOR', '#FFFFFF'),
            'font_size': int(os.getenv('FONT_SIZE', '1')),
            'font_name': os.getenv('FONT_NAME', 'mainTitle'),

            # 其他配置
            'mask_region': os.getenv('MASK_REGION'),
            'scale': float(os.getenv('SCALE', '1.0')),
            'move_h': int(os.getenv('MOVE_H', '0')),
            'move_v': int(os.getenv('MOVE_V', '0')),
            'audio_format': int(os.getenv('AUDIO_FORMAT', '1')),
            'interactive_mode': int(os.getenv('INTERACTIVE_MODE', '0')),
        }

    @staticmethod
    def _log_config_summary(config: AvatarConfig, logger):
        """记录配置摘要（隐藏敏感信息）"""
        logger.info("📋 配置摘要:")
        logger.info(f"   - 应用ID: {config.app_id}")
        logger.info(
            f"   - 应用Key: {'*' * (len(config.app_key) - 4) + config.app_key[-4:] if len(config.app_key) > 4 else '****'}")
        logger.info(f"   - 形象ID: {config.avatar_id}")
        logger.info(f"   - 发音人: {config.vcn}")
        logger.info(f"   - 分辨率: {config.width}x{config.height}")
        logger.info(f"   - 推流协议: {config.stream_protocol}")
        logger.info(f"   - 码率: {config.stream_bitrate}k")

    @staticmethod
    def validate_config(config: AvatarConfig) -> bool:
        """
        验证配置是否有效
        根据讯飞虚拟人实时交互API文档进行参数验证

        Args:
            config: 配置对象

        Returns:
            bool: 配置是否有效
        """
        # 检查必需字段
        if not all([config.app_id, config.app_key, config.app_secret, config.avatar_id]):
            return False

        # 检查字符串长度限制
        if len(config.app_id) > 50:  # API文档: maxLength 50
            return False
        if len(config.app_key) < 10 or len(config.app_secret) < 10:
            return False

        # 检查推流配置参数范围
        # stream.fps: 13-25 (API文档规定)
        if not (13 <= config.stream_fps <= 25):
            return False

        # stream.bitrate: 200-20000 kb (API文档规定)
        if not (200 <= config.stream_bitrate <= 20000):
            return False

        # 分辨率: 4的倍数 [300,4096] (API文档规定)
        if not (300 <= config.width <= 4096) or config.width % 4 != 0:
            return False
        if not (300 <= config.height <= 4096) or config.height % 4 != 0:
            return False

        # TTS参数: [0,100] (API文档规定)
        if not (0 <= config.tts_speed <= 100):
            return False
        if not (0 <= config.tts_pitch <= 100):
            return False
        if not (0 <= config.tts_volume <= 100):
            return False

        # 虚拟人缩放: [0.1, 1.0] (API文档规定)
        if not (0.1 <= config.scale <= 1.0):
            return False

        # 虚拟人平移距离: [-4096, +4096] (API文档规定)
        if not (-4096 <= config.move_h <= 4096):
            return False
        if not (-4096 <= config.move_v <= 4096):
            return False

        # 推流协议检查 (API文档支持的协议)
        if config.stream_protocol not in ['rtmp', 'xrtc', 'webrtc', 'flv']:
            return False

        # 透明通道推流: 0或1
        if hasattr(config, 'stream_alpha') and config.stream_alpha not in [0, 1]:
            return False

        # 音频格式: 1(16k) 或 2(24k) (API文档规定)
        if config.audio_format not in [1, 2]:
            return False

        # 交互模式: 0(追加) 或 1(打断) (API文档规定)
        if config.interactive_mode not in [0, 1]:
            return False

        # 动作配置: 0(关闭) 或 1(开启)
        if hasattr(config, 'air_enabled') and config.air_enabled not in [0, 1]:
            return False
        if hasattr(config, 'add_nonsemantic') and config.add_nonsemantic not in [0, 1]:
            return False

        # 字幕配置验证
        if hasattr(config, 'subtitle_enabled') and config.subtitle_enabled not in [0, 1]:
            return False
        if hasattr(config, 'font_size') and not (1 <= config.font_size <= 10):  # API文档: 1-10
            return False

        # 字体样式检查 (API文档支持的字体)
        valid_fonts = [
            'Sanji.Suxian.Simple',
            'Honglei.Runninghand.Sim',
            'Hunyuan.Gothic.Bold',
            'Huayuan.Gothic.Regular',
            'mainTitle'
        ]
        if hasattr(config, 'font_name') and config.font_name and config.font_name not in valid_fonts:
            return False

        # 颜色格式检查 (十六进制颜色)
        if hasattr(config, 'font_color') and config.font_color:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', config.font_color):
                return False

        return True

    @staticmethod
    def validate_config_detailed(config: AvatarConfig) -> Dict[str, List[str]]:
        """
        详细验证配置是否有效，返回具体的错误信息

        Args:
            config: 配置对象

        Returns:
            Dict[str, List[str]]: 验证结果，包含errors和warnings两个列表
        """
        errors = []
        warnings = []

        # 检查必需字段
        if not config.app_id:
            errors.append("缺少必需参数: app_id")
        elif len(config.app_id) > 50:
            errors.append(f"app_id长度超过限制: {len(config.app_id)} > 50")

        if not config.app_key:
            errors.append("缺少必需参数: app_key")
        elif len(config.app_key) < 10:
            warnings.append(f"app_key长度可能过短: {len(config.app_key)} < 10")

        if not config.app_secret:
            errors.append("缺少必需参数: app_secret")
        elif len(config.app_secret) < 10:
            warnings.append(f"app_secret长度可能过短: {len(config.app_secret)} < 10")

        if not config.avatar_id:
            errors.append("缺少必需参数: avatar_id")

        # 推流配置验证
        if not (13 <= config.stream_fps <= 25):
            errors.append(f"推流帧率超出范围: {config.stream_fps} (应在13-25之间)")

        if not (200 <= config.stream_bitrate <= 20000):
            errors.append(
                f"推流码率超出范围: {config.stream_bitrate} (应在200-20000kb之间)")

        # 分辨率验证
        if not (300 <= config.width <= 4096):
            errors.append(f"分辨率宽度超出范围: {config.width} (应在300-4096之间)")
        elif config.width % 4 != 0:
            errors.append(f"分辨率宽度必须是4的倍数: {config.width}")

        if not (300 <= config.height <= 4096):
            errors.append(f"分辨率高度超出范围: {config.height} (应在300-4096之间)")
        elif config.height % 4 != 0:
            errors.append(f"分辨率高度必须是4的倍数: {config.height}")

        # TTS参数验证
        if not (0 <= config.tts_speed <= 100):
            errors.append(f"TTS语速超出范围: {config.tts_speed} (应在0-100之间)")

        if not (0 <= config.tts_pitch <= 100):
            errors.append(f"TTS音调超出范围: {config.tts_pitch} (应在0-100之间)")

        if not (0 <= config.tts_volume <= 100):
            errors.append(f"TTS音量超出范围: {config.tts_volume} (应在0-100之间)")

        # 虚拟人显示参数验证
        if not (0.1 <= config.scale <= 1.0):
            errors.append(f"虚拟人缩放比例超出范围: {config.scale} (应在0.1-1.0之间)")

        if not (-4096 <= config.move_h <= 4096):
            errors.append(f"虚拟人水平移动距离超出范围: {config.move_h} (应在-4096到+4096之间)")

        if not (-4096 <= config.move_v <= 4096):
            errors.append(f"虚拟人垂直移动距离超出范围: {config.move_v} (应在-4096到+4096之间)")

        # 协议和格式验证
        valid_protocols = ['rtmp', 'xrtc', 'webrtc', 'flv']
        if config.stream_protocol not in valid_protocols:
            errors.append(
                f"不支持的推流协议: {config.stream_protocol} (支持: {', '.join(valid_protocols)})")

        if config.audio_format not in [1, 2]:
            errors.append(
                f"不支持的音频格式: {config.audio_format} (支持: 1=16k, 2=24k)")

        if config.interactive_mode not in [0, 1]:
            errors.append(
                f"不支持的交互模式: {config.interactive_mode} (支持: 0=追加, 1=打断)")

        # 可选参数验证
        if hasattr(config, 'stream_alpha') and config.stream_alpha not in [0, 1]:
            errors.append(f"透明通道参数错误: {config.stream_alpha} (支持: 0=关闭, 1=开启)")

        if hasattr(config, 'air_enabled') and config.air_enabled not in [0, 1]:
            errors.append(f"自动动作参数错误: {config.air_enabled} (支持: 0=关闭, 1=开启)")

        if hasattr(config, 'add_nonsemantic') and config.add_nonsemantic not in [0, 1]:
            errors.append(
                f"无指向性动作参数错误: {config.add_nonsemantic} (支持: 0=关闭, 1=开启)")

        if hasattr(config, 'subtitle_enabled') and config.subtitle_enabled not in [0, 1]:
            errors.append(
                f"字幕开关参数错误: {config.subtitle_enabled} (支持: 0=关闭, 1=开启)")

        if hasattr(config, 'font_size') and not (1 <= config.font_size <= 10):
            errors.append(f"字幕字体大小超出范围: {config.font_size} (应在1-10之间)")

        # 字体样式验证
        if hasattr(config, 'font_name') and config.font_name:
            valid_fonts = [
                'Sanji.Suxian.Simple',
                'Honglei.Runninghand.Sim',
                'Hunyuan.Gothic.Bold',
                'Huayuan.Gothic.Regular',
                'mainTitle'
            ]
            if config.font_name not in valid_fonts:
                errors.append(
                    f"不支持的字体样式: {config.font_name} (支持: {', '.join(valid_fonts)})")

        # 颜色格式验证
        if hasattr(config, 'font_color') and config.font_color:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', config.font_color):
                errors.append(
                    f"字体颜色格式错误: {config.font_color} (应为十六进制颜色，如#FFFFFF)")

        # 特殊组合验证
        if config.stream_protocol == 'xrtc' and hasattr(config, 'stream_alpha') and config.stream_alpha == 1:
            # xrtc协议支持透明通道，这是正常的
            pass
        elif hasattr(config, 'stream_alpha') and config.stream_alpha == 1:
            warnings.append("透明通道仅在xrtc协议下生效，当前协议为: " + config.stream_protocol)

        return {
            'errors': errors,
            'warnings': warnings,
            'is_valid': len(errors) == 0
        }

    @staticmethod
    def create_env_template(file_path: str = ".env.example") -> None:
        """
        创建环境变量模板文件
        根据API文档生成完整的配置模板

        Args:
            file_path: 模板文件路径
        """
        template_content = """# 讯飞虚拟人SDK配置文件模板
# 复制此文件为 .env 并填入您的真实配置
# 参考: https://www.yuque.com/xnrpt/bbc1du/xamwb751mbpgeg2o

# ============ 必需配置 ============
# 请在讯飞虚拟人交互平台申请以下参数

# 应用基础信息（必填）
APP_ID=your_app_id                    # 应用ID，最大长度50字符
APP_KEY=your_app_key                  # 应用密钥
APP_SECRET=your_app_secret            # 应用秘钥

# 虚拟人形象配置（必填）
AVATAR_ID=your_avatar_id              # 虚拟人形象ID，请到交互平台获取

# ============ 可选配置 ============

# 发音人配置
VCN=x4_xiaozhong                      # 发音人ID，请到交互平台-声音列表获取

# WebSocket连接配置
BASE_URL=wss://avatar.cn-huadong-1.xf-yun.com/v1/interact

# ============ 推流配置 ============
# 推流协议: rtmp, xrtc, webrtc, flv
STREAM_PROTOCOL=webrtc

# 推流帧率: 13-25
STREAM_FPS=25

# 推流码率: 200-20000 (单位: kb)
STREAM_BITRATE=2000

# 透明通道推流: 0=关闭, 1=开启 (仅xrtc协议生效)
STREAM_ALPHA=0

# 分辨率 (必须是4的倍数，范围: 300-4096)
WIDTH=720
HEIGHT=1280

# ============ TTS配置 ============
# 语音参数范围: 0-100
TTS_SPEED=50                          # 语音速度
TTS_PITCH=50                          # 语音音调
TTS_VOLUME=50                         # 语音音量

# ============ 虚拟人显示配置 ============
# 虚拟人缩放: 0.1-1.0
SCALE=1.0

# 虚拟人位置偏移: -4096到+4096 (像素)
MOVE_H=0                              # 水平偏移 (负数左移，正数右移)
MOVE_V=0                              # 垂直偏移 (负数下移，正数上移)

# 虚拟人裁剪区域 (格式: [左,上,右,下])
# MASK_REGION=[0,0,1080,1920]

# ============ 动作配置 ============
# 动作开关: 0=关闭, 1=开启
AIR_ENABLED=0                         # 自动动作
ADD_NONSEMANTIC=0                     # 无指向性动作

# ============ 字幕配置 ============
# 字幕开关: 0=关闭, 1=开启
SUBTITLE_ENABLED=0

# 字幕样式
FONT_COLOR=#FFFFFF                    # 字体颜色 (十六进制)
FONT_SIZE=1                           # 字体大小: 1-10
FONT_NAME=mainTitle                   # 字体样式: mainTitle, Sanji.Suxian.Simple 等

# 字幕位置 (需配合width/height使用)
# POSITION_X=0                        # 左右位置: 0-10000
# POSITION_Y=0                        # 上下位置: 0-10000

# ============ 其他配置 ============
# 音频格式: 1=16k, 2=24k
AUDIO_FORMAT=1

# 交互模式: 0=追加, 1=打断
INTERACTIVE_MODE=0

# ============ 高级配置示例 ============
# 用于 advanced_example.py，会覆盖上面的基础配置

# 高分辨率推流
# STREAM_BITRATE=3000
# WIDTH=1080
# HEIGHT=1920

# 优化的TTS设置
# TTS_SPEED=60
# TTS_PITCH=55
# TTS_VOLUME=80

# 启用高级功能
# AIR_ENABLED=1
# ADD_NONSEMANTIC=1
# SUBTITLE_ENABLED=1
# FONT_COLOR=#00FF00
# FONT_SIZE=3
# SCALE=0.8
# MOVE_H=50
# MOVE_V=-100

# ============ 安全提醒 ============
# 1. 请勿将包含真实密钥的.env文件提交到版本控制系统
# 2. 定期更换API密钥以确保安全
# 3. 在生产环境中使用环境变量而非.env文件
# 4. 确保.env文件权限设置正确（只有所有者可读写）
# 5. 所有参数都需符合API文档规定的范围和格式
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template_content)

        print(f"✅ 环境变量模板已创建: {file_path}")
        print("📋 模板包含:")
        print("   - 完整的参数说明和取值范围")
        print("   - 基于API文档的准确配置")
        print("   - 安全使用提醒")
        print("   - 高级功能配置示例")

    @staticmethod
    def get_safe_config_dict(config: AvatarConfig) -> Dict[str, Any]:
        """
        获取安全的配置字典（隐藏敏感信息）

        Args:
            config: 配置对象

        Returns:
            Dict[str, Any]: 安全的配置字典
        """
        config_dict = config.to_dict()

        # 隐藏敏感信息
        for key in ConfigLoader.SENSITIVE_KEYS:
            if key.lower() in config_dict:
                value = config_dict[key.lower()]
                if isinstance(value, str) and len(value) > 4:
                    config_dict[key.lower()] = '*' * \
                        (len(value) - 4) + value[-4:]
                else:
                    config_dict[key.lower()] = '****'

        return config_dict
