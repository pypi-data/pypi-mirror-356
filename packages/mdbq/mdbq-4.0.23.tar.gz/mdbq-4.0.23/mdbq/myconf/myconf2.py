import re
from typing import Dict, Any, Optional, Union, List, Tuple, Type, TypeVar
from pathlib import Path
from mdbq.log import mylogger
from dataclasses import dataclass, field
from enum import Enum
import time

logger = mylogger.MyLogger(
    logging_mode='both',
    log_level='info',
    log_format='json',
    max_log_size=50,
    backup_count=5,
    enable_async=False,  # 是否启用异步日志
    sample_rate=1,  # 采样DEBUG/INFO日志
    sensitive_fields=[],  #  敏感字段过滤
    enable_metrics=False,  # 是否启用性能指标
)

T = TypeVar('T')  # 类型变量


class ConfigError(Exception):
    """配置相关的基础异常类"""
    def __init__(self, message: str, file_path: Optional[Union[str, Path]] = None, 
                 section: Optional[str] = None, key: Optional[str] = None):
        self.message = message
        self.file_path = str(file_path) if file_path else None
        self.section = section
        self.key = key
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """格式化错误消息"""
        parts = [self.message]
        if self.file_path:
            parts.append(f"文件: {self.file_path}")
        if self.section:
            parts.append(f"节: [{self.section}]")
        if self.key:
            parts.append(f"键: {self.key}")
        return " | ".join(parts)


class ConfigFileNotFoundError(ConfigError):
    """配置文件不存在异常"""
    def __init__(self, file_path: Union[str, Path]):
        super().__init__("配置文件不存在", file_path=file_path)


class ConfigReadError(ConfigError):
    """读取配置文件失败异常"""
    def __init__(self, file_path: Union[str, Path], original_error: Exception):
        super().__init__(
            f"读取配置文件失败: {str(original_error)}",
            file_path=file_path
        )
        self.original_error = original_error


class ConfigWriteError(ConfigError):
    """写入配置文件失败异常"""
    def __init__(self, file_path: Union[str, Path], original_error: Exception):
        super().__init__(
            f"写入配置文件失败: {str(original_error)}",
            file_path=file_path
        )
        self.original_error = original_error


class ConfigValueError(ConfigError):
    """配置值无效异常"""
    def __init__(self, message: str, file_path: Union[str, Path], 
                 section: Optional[str] = None, key: Optional[str] = None):
        super().__init__(message, file_path=file_path, section=section, key=key)


class ConfigSectionNotFoundError(ConfigError):
    """配置节不存在异常"""
    def __init__(self, file_path: Union[str, Path], section: str):
        super().__init__(
            f"配置节不存在",
            file_path=file_path,
            section=section
        )


class ConfigKeyNotFoundError(ConfigError):
    """配置键不存在异常"""
    def __init__(self, file_path: Union[str, Path], section: str, key: str):
        super().__init__(
            f"配置键不存在",
            file_path=file_path,
            section=section,
            key=key
        )


class CommentStyle(Enum):
    """配置文件支持的注释风格"""
    HASH = '#'  # Python风格注释
    DOUBLE_SLASH = '//'  # C风格注释
    SEMICOLON = ';'  # INI风格注释


@dataclass
class ConfigOptions:
    """配置解析器选项"""
    comment_styles: List[CommentStyle] = field(default_factory=lambda: [CommentStyle.HASH, CommentStyle.DOUBLE_SLASH])
    encoding: str = 'utf-8'
    auto_create: bool = False
    strip_values: bool = True
    preserve_comments: bool = True
    default_section: str = 'DEFAULT'
    separators: List[str] = field(default_factory=lambda: ['=', ':', '：'])
    cache_ttl: int = 300  # 5分钟缓存过期
    validate_keys: bool = True
    key_pattern: str = r'^[a-zA-Z0-9_\-\.]+$'
    case_sensitive: bool = False


class ConfigParser:
    """配置文件解析器"""
    
    def __init__(self, options: Optional[ConfigOptions] = None):
        self.options = options or ConfigOptions()
        self._config_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._comments_cache: Dict[str, Dict[str, List[str]]] = {}
        self._section_map: Dict[str, Dict[str, str]] = {}
        self._current_file: Optional[Path] = None
    
    def __enter__(self) -> 'ConfigParser':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[Any]) -> None:
        self._current_file = None

    def open(self, file_path: Union[str, Path]) -> 'ConfigParser':
        """打开配置文件"""
        file_path = Path(file_path)
        if not file_path.exists() and not self.options.auto_create:
            raise ConfigFileNotFoundError(file_path)
        self._current_file = file_path
        return self

    def _ensure_file_open(self) -> None:
        """确保文件已打开"""
        if self._current_file is None:
            raise ConfigError("未打开任何配置文件，请先调用 open() 方法")

    def _is_comment_line(self, line: str) -> bool:
        """判断是否为注释行"""
        stripped = line.strip()
        return any(stripped.startswith(style.value) for style in self.options.comment_styles)
    
    def _extract_comment(self, line: str) -> Tuple[str, str]:
        """从行中提取注释"""
        for style in self.options.comment_styles:
            comment_match = re.search(fr'\s+{re.escape(style.value)}.*$', line)
            if comment_match:
                return line[:comment_match.start()].strip(), comment_match.group(0)
        return line.strip(), ''
    
    def _split_key_value(self, line: str) -> Optional[Tuple[str, str]]:
        """分割配置行为键值对"""
        for sep in self.options.separators:
            if sep in line:
                key_part, value_part = line.split(sep, 1)
                return key_part.strip(), value_part
        
        for sep in [':', '：']:
            if sep in line:
                pattern = fr'\s*{re.escape(sep)}\s*'
                parts = re.split(pattern, line, 1)
                if len(parts) == 2:
                    return parts[0].strip(), parts[1]
        
        return None
    
    def _validate_key(self, key: str) -> bool:
        """验证键名是否合法"""
        if not self.options.validate_keys:
            return True
        return bool(re.match(self.options.key_pattern, key))
    
    def _get_cached_config(self, file_path: str) -> Optional[Dict[str, Any]]:
        """获取缓存的配置"""
        if file_path not in self._config_cache or file_path not in self._cache_timestamps:
            return None
        
        if time.time() - self._cache_timestamps[file_path] > self.options.cache_ttl:
            return None
        
        return self._config_cache[file_path]
    
    def _update_cache(self, file_path: str, config: Dict[str, Any]) -> None:
        """更新配置缓存"""
        self._config_cache[file_path] = config
        self._cache_timestamps[file_path] = time.time()
    
    def _normalize_section(self, section: str) -> str:
        """标准化节名称"""
        return section if self.options.case_sensitive else section.lower()
    
    def _get_original_section(self, file_path: str, normalized_section: str) -> Optional[str]:
        """获取原始节名称"""
        if self.options.case_sensitive:
            return normalized_section
        return self._section_map.get(file_path, {}).get(normalized_section)
    
    def _update_section_map(self, file_path: str, section: str) -> None:
        """更新节名称映射"""
        if not self.options.case_sensitive:
            normalized = self._normalize_section(section)
            if file_path not in self._section_map:
                self._section_map[file_path] = {}
            self._section_map[file_path][normalized] = section
    
    def _clear_cache(self, file_path: Optional[str] = None) -> None:
        """清除配置缓存"""
        if file_path:
            self._config_cache.pop(file_path, None)
            self._cache_timestamps.pop(file_path, None)
            self._comments_cache.pop(file_path, None)
            self._section_map.pop(file_path, None)
        else:
            self._config_cache.clear()
            self._cache_timestamps.clear()
            self._comments_cache.clear()
            self._section_map.clear()
    
    def _convert_value(self, value: str, target_type: Type[T], file_path: Optional[Union[str, Path]] = None, key: Optional[str] = None) -> T:
        """转换配置值到指定类型"""
        try:
            if target_type == bool:
                return bool(value.lower() in ('true', 'yes', '1', 'on'))
            elif target_type == list:
                if not value.strip():
                    return []
                for sep in [',', ';', '|', ' ']:
                    if sep in value:
                        return [item.strip() for item in value.split(sep) if item.strip()]
                return [value.strip()]
            elif target_type == tuple:
                if not value.strip():
                    return ()
                for sep in [',', ';', '|', ' ']:
                    if sep in value:
                        return tuple(item.strip() for item in value.split(sep) if item.strip())
                return (value.strip(),)
            elif target_type == set or target_type == frozenset:
                if not value.strip():
                    return set() if target_type == set else frozenset()
                for sep in [',', ';', '|', ' ']:
                    if sep in value:
                        items = [item.strip() for item in value.split(sep) if item.strip()]
                        return set(items) if target_type == set else frozenset(items)
                return set([value.strip()]) if target_type == set else frozenset([value.strip()])
            elif target_type == dict:
                if not value.strip():
                    return {}
                result = {}
                for sep in [',', ';', '|']:
                    if sep in value:
                        pairs = [pair.strip() for pair in value.split(sep) if pair.strip()]
                        for pair in pairs:
                            if '=' in pair:
                                key_, val = pair.split('=', 1)
                                result[key_.strip()] = val.strip()
                        return result
                if '=' in value:
                    key_, val = value.split('=', 1)
                    return {key_.strip(): val.strip()}
                return {}
            elif target_type == int:
                value = value.strip().lower()
                if value.startswith('0x'):
                    return int(value, 16)
                elif value.startswith('0o'):
                    return int(value, 8)
                elif value.startswith('0b'):
                    return int(value, 2)
                return int(value)
            elif target_type == float:
                return float(value)
            elif target_type == complex:
                return complex(value)
            elif target_type == bytes:
                return value.encode('utf-8')
            elif target_type == bytearray:
                return bytearray(value.encode('utf-8'))
            elif target_type == range:
                parts = value.split(':')
                if len(parts) == 2:
                    return range(int(parts[0]), int(parts[1]))
                elif len(parts) == 3:
                    return range(int(parts[0]), int(parts[1]), int(parts[2]))
                raise ValueError("Invalid range format")
            return target_type(value)
        except (ValueError, TypeError) as e:
            raise ConfigValueError(
                f"无法将值 '{value}' 转换为类型 {target_type.__name__}",
                file_path=file_path,
                key=key
            )
    
    def get_value(self, file_path: Optional[Union[str, Path]] = None, key: str = None, 
                 section: Optional[str] = None, default: Any = None,
                 value_type: Optional[Type[T]] = None) -> T:
        """获取指定配置项的值"""
        if file_path is None:
            self._ensure_file_open()
            file_path = self._current_file
        if not self._validate_key(key):
            raise ConfigValueError(f"无效的键名: {key}", file_path=file_path, key=key)
        config = self.read(file_path)
        section = section or self.options.default_section
        normalized_section = self._normalize_section(section)
        original_section = self._get_original_section(str(file_path), normalized_section)
        if original_section is None:
            if default is not None:
                return default
            raise ConfigSectionNotFoundError(file_path, section)
        if key not in config[original_section]:
            if default is not None:
                return default
            raise ConfigKeyNotFoundError(file_path, original_section, key)
        value = config[original_section][key]
        if value_type is not None:
            return self._convert_value(value, value_type, file_path=file_path, key=key)
        return value
    
    def get_values(self, keys: List[Tuple[str, str]], 
                  file_path: Optional[Union[str, Path]] = None,
                  defaults: Optional[Dict[str, Any]] = None,
                  value_types: Optional[Dict[str, Type]] = None) -> Dict[str, Any]:
        """批量获取多个配置项的值"""
        if file_path is None:
            self._ensure_file_open()
            file_path = self._current_file
        defaults = defaults or {}
        value_types = value_types or {}
        result = {}
        
        for section, key in keys:
            try:
                value = self.get_value(
                    file_path=file_path,
                    key=key,
                    section=section,
                    default=defaults.get(key),
                    value_type=value_types.get(key)
                )
                result[key] = value
            except (ConfigSectionNotFoundError, ConfigKeyNotFoundError) as e:
                if key in defaults:
                    result[key] = defaults[key]
                else:
                    raise e
                    
        return result

    def get_section_values(self, keys: List[str],
                          section: Optional[str] = None,
                          file_path: Optional[Union[str, Path]] = None,
                          defaults: Optional[Dict[str, Any]] = None,
                          value_types: Optional[Dict[str, Type]] = None) -> Tuple[Any, ...]:
        """获取指定节点下多个键的值元组"""
        if file_path is None:
            self._ensure_file_open()
            file_path = self._current_file
        defaults = defaults or {}
        value_types = value_types or {}
        result = []
        
        for key in keys:
            try:
                value = self.get_value(
                    file_path=file_path,
                    key=key,
                    section=section,
                    default=defaults.get(key),
                    value_type=value_types.get(key)
                )
                result.append(value)
            except (ConfigSectionNotFoundError, ConfigKeyNotFoundError) as e:
                if key in defaults:
                    result.append(defaults[key])
                else:
                    raise e
                    
        return tuple(result)
    
    def set_value(self, key: str, value: Any,
                 section: Optional[str] = None,
                 file_path: Optional[Union[str, Path]] = None,
                 value_type: Optional[Type] = None) -> None:
        """设置指定配置项的值"""
        if file_path is None:
            self._ensure_file_open()
            file_path = self._current_file
        if not self._validate_key(key):
            raise ConfigValueError(f"无效的键名: {key}", file_path=file_path, key=key)
        section = section or self.options.default_section
        original_lines = []
        if file_path.exists():
            with open(file_path, 'r', encoding=self.options.encoding) as file:
                original_lines = file.readlines()
        config = self.read(file_path)
        if section not in config:
            config[section] = {}
        if value_type is not None:
            try:
                if value_type == bool:
                    if isinstance(value, str):
                        value = value.lower() in ('true', 'yes', '1', 'on')
                    else:
                        value = bool(value)
                else:
                    value = value_type(value)
            except (ValueError, TypeError) as e:
                raise ConfigValueError(
                    f"无法将值 '{value}' 转换为类型 {value_type.__name__}",
                    file_path=file_path,
                    section=section,
                    key=key
                )
        if isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)
        config[section][key] = value
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding=self.options.encoding) as file:
                current_section = self.options.default_section
                section_separators = {}
                for line in original_lines:
                    stripped_line = line.strip()
                    if not stripped_line:
                        file.write(line)
                        continue
                    if stripped_line.startswith('[') and stripped_line.endswith(']'):
                        current_section = stripped_line[1:-1]
                        file.write(line)
                        continue
                    if self._is_comment_line(stripped_line):
                        file.write(line)
                        continue
                    key_value = self._split_key_value(stripped_line)
                    if key_value:
                        orig_key, orig_value = key_value
                        for sep in self.options.separators:
                            if sep in line:
                                section_separators.setdefault(current_section, {})[orig_key] = sep
                                break
                        if current_section == section and orig_key == key:
                            separator = section_separators.get(current_section, {}).get(orig_key, self.options.separators[0])
                            comment = ''
                            for style in self.options.comment_styles:
                                comment_match = re.search(fr'\s+{re.escape(style.value)}.*$', line)
                                if comment_match:
                                    comment = comment_match.group(0)
                                    break
                            file.write(f'{key}{separator}{value}{comment}\n')
                        else:
                            file.write(line)
                    else:
                        file.write(line)
                if section not in [line.strip()[1:-1] for line in original_lines if line.strip().startswith('[') and line.strip().endswith(']')]:
                    file.write(f'\n[{section}]\n')
                    file.write(f'{key}={value}\n')
            self._clear_cache(str(file_path))
        except Exception as e:
            raise ConfigWriteError(file_path, e)
    
    def read(self, file_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """读取配置文件内容"""
        if file_path is None:
            self._ensure_file_open()
            file_path = self._current_file
        else:
            file_path = Path(file_path)
        
        cached_config = self._get_cached_config(str(file_path))
        if cached_config is not None:
            return cached_config
        
        if not file_path.exists():
            if not self.options.auto_create:
                raise ConfigFileNotFoundError(file_path)
            logger.info(f'配置文件不存在，将创建: {file_path}')
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            return {}
        
        try:
            with open(file_path, 'r', encoding=self.options.encoding) as file:
                config = {}
                current_section = self.options.default_section
                section_comments = []
                
                for line in file:
                    stripped_line = line.strip()
                    
                    if not stripped_line or self._is_comment_line(stripped_line):
                        if self.options.preserve_comments:
                            section_comments.append(line.rstrip())
                        continue
                    
                    if stripped_line.startswith('[') and stripped_line.endswith(']'):
                        current_section = stripped_line[1:-1]
                        if not self._validate_key(current_section):
                            raise ConfigValueError(
                                f"无效的节名: {current_section}",
                                file_path=file_path,
                                section=current_section
                            )
                        self._update_section_map(str(file_path), current_section)
                        if current_section not in config:
                            config[current_section] = {}
                        if self.options.preserve_comments:
                            self._comments_cache.setdefault(str(file_path), {}).setdefault(current_section, []).extend(section_comments)
                            section_comments = []
                        continue
                    
                    key_value = self._split_key_value(stripped_line)
                    if key_value:
                        key, value = key_value
                        if not self._validate_key(key):
                            raise ConfigValueError(
                                f"无效的键名: {key}",
                                file_path=file_path,
                                section=current_section,
                                key=key
                            )
                        value, comment = self._extract_comment(value)
                        
                        if self.options.strip_values:
                            value = value.strip()
                        
                        if current_section not in config:
                            config[current_section] = {}
                        
                        config[current_section][key] = value
                        if self.options.preserve_comments and comment:
                            self._comments_cache.setdefault(str(file_path), {}).setdefault(current_section, []).append(comment)
                
                self._update_cache(str(file_path), config)
                return config
                
        except Exception as e:
            raise ConfigReadError(file_path, e)


def main() -> None:
    """示例用法"""
    config_file = Path('/Users/xigua/spd.txt')
    try:
        # 方式1：使用上下文管理器
        with ConfigParser() as parser:
            parser.open(config_file)
            host, port, username, password = parser.get_section_values(
                keys=['host', 'port', 'username', 'password'],
                section='mysql'
            )
            print("方式1结果:", host, port, username, password)
            parser.set_value('username', 'root', section='mysql')
            parser.set_value('port', 3306, section='mysql')
        # 方式2：链式调用
        parser = ConfigParser()
        host, port, username, password = parser.open(config_file).get_section_values(
            keys=['host', 'port', 'username', 'password'],
            section='mysql'
        )
        print("\n方式2结果:", host, port, username, password)
        # 方式3：传统方式
        parser = ConfigParser()
        host, port, username, password = parser.get_section_values(
            file_path=config_file,
            section='mysql',
            keys=['host', 'port', 'username', 'password']
        )
        print("\n方式3结果:", host, port, username, password)
    except Exception as e:
        print(f"配置文件操作异常: {e}")


if __name__ == '__main__':
    main()
