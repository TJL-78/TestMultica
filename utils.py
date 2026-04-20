"""
日志工具模块
提供灵活的日志记录功能，支持控制台和文件输出
"""

import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import os


class LoggerConfig:
    """日志配置类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'date_format': '%Y-%m-%d %H:%M:%S',
        'console': True,
        'file': False,
        'file_path': 'logs/app.log',
        'file_mode': 'a',
        'max_bytes': 10485760,  # 10MB
        'backup_count': 5,
    }
    
    def __init__(self, **kwargs):
        """初始化日志配置
        
        Args:
            **kwargs: 配置参数，可覆盖默认配置
                level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                format: 日志格式字符串
                date_format: 日期时间格式
                console: 是否启用控制台输出
                file: 是否启用文件输出
                file_path: 日志文件路径
                file_mode: 文件打开模式 ('a' 追加, 'w' 覆盖)
                max_bytes: 日志文件最大字节数（用于轮转）
                backup_count: 保留的备份文件数量
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(kwargs)
        
        # 转换字符串形式的日志级别
        if isinstance(self.config['level'], str):
            self.config['level'] = getattr(logging, self.config['level'].upper())
    
    def get(self, key: str, default=None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def update(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)


class LogManager:
    """日志管理器"""
    
    _loggers: Dict[str, logging.Logger] = {}
    _default_config = LoggerConfig()
    
    @classmethod
    def get_logger(cls, name: str = None, config: Optional[LoggerConfig] = None) -> logging.Logger:
        """获取或创建日志记录器
        
        Args:
            name: 日志记录器名称，如果为None则使用根记录器
            config: 日志配置，如果为None则使用默认配置
            
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        if name is None:
            name = 'root'
        
        # 如果已经存在该名称的记录器，直接返回
        if name in cls._loggers:
            return cls._loggers[name]
        
        # 使用提供的配置或默认配置
        if config is None:
            config = cls._default_config
        
        # 创建记录器
        logger = logging.getLogger(name)
        logger.setLevel(config.get('level'))
        
        # 清除现有的处理器，避免重复添加
        logger.handlers.clear()
        
        # 添加控制台处理器
        if config.get('console'):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(config.get('level'))
            console_formatter = logging.Formatter(
                config.get('format'),
                datefmt=config.get('date_format')
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # 添加文件处理器
        if config.get('file'):
            file_path = config.get('file_path')
            
            # 确保日志目录存在
            log_dir = os.path.dirname(file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # 创建文件处理器
            if config.get('max_bytes') > 0:
                # 使用轮转文件处理器
                from logging.handlers import RotatingFileHandler
                file_handler = RotatingFileHandler(
                    filename=file_path,
                    mode=config.get('file_mode'),
                    maxBytes=config.get('max_bytes'),
                    backupCount=config.get('backup_count')
                )
            else:
                # 使用普通文件处理器
                file_handler = logging.FileHandler(
                    filename=file_path,
                    mode=config.get('file_mode')
                )
            
            file_handler.setLevel(config.get('level'))
            file_formatter = logging.Formatter(
                config.get('format'),
                datefmt=config.get('date_format')
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        # 保存记录器
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def set_default_config(cls, config: LoggerConfig):
        """设置默认配置"""
        cls._default_config = config
    
    @classmethod
    def get_default_config(cls) -> LoggerConfig:
        """获取默认配置"""
        return cls._default_config


# 便捷函数
def get_logger(name: str = None, **kwargs) -> logging.Logger:
    """获取日志记录器的便捷函数
    
    Args:
        name: 日志记录器名称
        **kwargs: 配置参数，将传递给LoggerConfig
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    config = None
    if kwargs:
        config = LoggerConfig(**kwargs)
    return LogManager.get_logger(name, config)


def setup_logging(config: Optional[LoggerConfig] = None):
    """设置根日志记录器
    
    Args:
        config: 日志配置
    """
    if config is None:
        config = LoggerConfig()
    
    # 配置根记录器
    root_logger = LogManager.get_logger('root', config)
    
    # 设置logging模块的默认记录器
    logging.basicConfig(
        level=config.get('level'),
        format=config.get('format'),
        datefmt=config.get('date_format'),
        handlers=[]  # 不添加处理器，由LogManager管理
    )


# 示例使用
def example_usage():
    """日志工具使用示例"""
    
    print("=" * 60)
    print("日志工具使用示例")
    print("=" * 60)
    
    # 示例1: 基本使用 - 控制台输出
    print("\n1. 基本使用 - 控制台输出:")
    logger1 = get_logger('example1')
    logger1.debug("这是一条DEBUG消息")
    logger1.info("这是一条INFO消息")
    logger1.warning("这是一条WARNING消息")
    logger1.error("这是一条ERROR消息")
    logger1.critical("这是一条CRITICAL消息")
    
    # 示例2: 自定义配置
    print("\n2. 自定义配置 - 文件和控制台输出:")
    config = LoggerConfig(
        level='DEBUG',
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        date_format='%H:%M:%S',
        console=True,
        file=True,
        file_path='logs/example.log',
        max_bytes=1024 * 1024,  # 1MB
        backup_count=3
    )
    logger2 = get_logger('example2', config=config)
    logger2.debug("调试信息")
    logger2.info("程序启动")
    logger2.warning("温度过高警告")
    logger2.error("传感器连接失败")
    
    # 示例3: 不同模块使用不同的日志记录器
    print("\n3. 不同模块使用不同的日志记录器:")
    
    # 传感器模块
    sensor_logger = get_logger('sensor', level='INFO')
    sensor_logger.info("传感器模块初始化完成")
    
    # 网络模块
    network_logger = get_logger('network', level='DEBUG')
    network_logger.debug("建立网络连接")
    network_logger.info("连接成功")
    
    # 数据库模块
    db_logger = get_logger('database', level='WARNING')
    db_logger.warning("数据库连接池接近上限")
    
    # 示例4: 异常日志记录
    print("\n4. 异常日志记录:")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger1.error("发生除零错误", exc_info=True)
    
    # 示例5: 带参数的日志
    print("\n5. 带参数的日志:")
    temperature = 25.5
    humidity = 60.2
    logger1.info("传感器数据 - 温度: %.1f°C, 湿度: %.1f%%", temperature, humidity)
    
    print("\n" + "=" * 60)
    print("示例完成，查看 logs/example.log 文件查看文件输出")
    print("=" * 60)


if __name__ == "__main__":
    # 运行示例
    example_usage()