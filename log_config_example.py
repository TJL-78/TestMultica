#!/usr/bin/env python3
"""
日志配置示例
展示不同的日志配置方案
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import get_logger, LoggerConfig


def development_config():
    """开发环境配置"""
    print("\n开发环境配置:")
    config = LoggerConfig(
        level='DEBUG',
        format='[%(asctime)s] %(levelname)-8s %(name)-20s: %(message)s',
        date_format='%H:%M:%S',
        console=True,
        file=True,
        file_path='logs/dev.log',
        max_bytes=5242880,  # 5MB
        backup_count=3
    )
    return config


def production_config():
    """生产环境配置"""
    print("\n生产环境配置:")
    config = LoggerConfig(
        level='INFO',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        date_format='%Y-%m-%d %H:%M:%S',
        console=False,  # 生产环境通常不输出到控制台
        file=True,
        file_path='logs/production.log',
        max_bytes=10485760,  # 10MB
        backup_count=10
    )
    return config


def debug_config():
    """调试配置"""
    print("\n调试配置:")
    config = LoggerConfig(
        level='DEBUG',
        format='%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s',
        date_format='%H:%M:%S',
        console=True,
        file=True,
        file_path='logs/debug.log',
        max_bytes=0,  # 不限制大小
        backup_count=0
    )
    return config


def minimal_config():
    """最小化配置"""
    print("\n最小化配置:")
    config = LoggerConfig(
        level='WARNING',  # 只记录警告及以上级别
        format='%(levelname)s: %(message)s',
        console=True,
        file=False
    )
    return config


def test_configurations():
    """测试不同的配置"""
    print("=" * 60)
    print("日志配置示例")
    print("=" * 60)
    
    # 测试开发环境配置
    dev_config = development_config()
    dev_logger = get_logger('dev', config=dev_config)
    dev_logger.debug("开发环境调试信息")
    dev_logger.info("开发环境启动")
    dev_logger.warning("开发环境警告")
    
    # 测试生产环境配置
    prod_config = production_config()
    prod_logger = get_logger('prod', config=prod_config)
    prod_logger.info("生产环境启动")
    prod_logger.error("生产环境错误")
    
    # 测试调试配置
    debug_config_obj = debug_config()
    debug_logger = get_logger('debug', config=debug_config_obj)
    debug_logger.debug("详细调试信息")
    
    # 测试最小化配置
    min_config = minimal_config()
    min_logger = get_logger('minimal', config=min_config)
    min_logger.info("这条信息不会被记录")  # INFO级别低于WARNING
    min_logger.warning("这条警告会被记录")
    
    print("\n" + "=" * 60)
    print("配置测试完成")
    print("查看 logs/ 目录下的不同日志文件")
    print("=" * 60)


def create_module_loggers():
    """为不同模块创建专门的日志记录器"""
    print("\n" + "=" * 60)
    print("模块化日志记录器示例")
    print("=" * 60)
    
    # 传感器模块
    sensor_logger = get_logger('sensor', level='INFO')
    sensor_logger.info("传感器模块初始化")
    
    # 网络模块
    network_logger = get_logger('network', level='DEBUG')
    network_logger.debug("网络连接建立中...")
    network_logger.info("网络连接成功")
    
    # 数据库模块
    db_logger = get_logger('database', level='WARNING')
    db_logger.info("数据库查询完成")  # 不会被记录
    db_logger.warning("数据库连接池接近上限")
    
    # 业务逻辑模块
    business_logger = get_logger('business', level='INFO')
    business_logger.info("业务处理开始")
    business_logger.error("业务处理失败")
    
    print("\n每个模块使用独立的日志记录器，便于:")
    print("1. 按模块过滤日志")
    print("2. 为不同模块设置不同日志级别")
    print("3. 跟踪特定模块的问题")


if __name__ == "__main__":
    test_configurations()
    create_module_loggers()