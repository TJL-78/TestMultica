#!/usr/bin/env python3
"""
日志工具测试脚本
演示如何在现有项目中使用日志工具
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import get_logger, LoggerConfig, setup_logging


def test_sensor_publisher():
    """模拟传感器发布器使用日志"""
    logger = get_logger('sensor.publisher')
    
    logger.info("传感器发布器启动")
    logger.debug("初始化FastDDS域参与者")
    
    # 模拟发布过程
    for i in range(3):
        temperature = 20.0 + i * 2.5
        logger.info("发布传感器数据 [ID: %d, 温度: %.2f°C]", i + 1, temperature)
    
    logger.warning("网络延迟较高")
    logger.info("传感器发布器停止")


def test_sensor_subscriber():
    """模拟传感器订阅器使用日志"""
    logger = get_logger('sensor.subscriber')
    
    logger.info("传感器订阅器启动")
    logger.debug("注册数据类型: SensorData")
    
    # 模拟接收过程
    received_data = [
        (1, 22.5),
        (2, 25.0),
        (3, 18.5)
    ]
    
    for sensor_id, temperature in received_data:
        logger.info("收到传感器数据 [ID: %d, 温度: %.2f°C]", sensor_id, temperature)
    
    logger.error("传感器3连接丢失")
    logger.info("传感器订阅器停止")


def test_custom_config():
    """测试自定义配置"""
    print("\n" + "=" * 60)
    print("测试自定义配置")
    print("=" * 60)
    
    # 创建自定义配置
    config = LoggerConfig(
        level='DEBUG',
        format='[%(asctime)s] %(levelname)-8s %(name)-20s: %(message)s',
        date_format='%H:%M:%S',
        console=True,
        file=True,
        file_path='logs/test.log',
        max_bytes=1024 * 1024,  # 1MB
        backup_count=2
    )
    
    # 使用自定义配置获取日志记录器
    custom_logger = get_logger('custom', config=config)
    
    custom_logger.debug("详细调试信息")
    custom_logger.info("自定义配置测试开始")
    custom_logger.warning("测试警告信息")
    custom_logger.error("测试错误信息")
    
    # 测试异常记录
    try:
        raise ValueError("测试异常")
    except ValueError as e:
        custom_logger.exception("捕获到异常: %s", str(e))


def main():
    """主函数"""
    print("日志工具测试")
    print("=" * 60)
    
    # 方法1: 使用默认配置
    print("\n方法1: 使用默认配置")
    default_logger = get_logger('test.default')
    default_logger.info("使用默认配置的日志记录器")
    
    # 方法2: 使用便捷函数直接配置
    print("\n方法2: 使用便捷函数直接配置")
    direct_logger = get_logger('test.direct', level='DEBUG', console=True)
    direct_logger.debug("直接配置的调试信息")
    direct_logger.info("直接配置的信息")
    
    # 测试不同模块
    print("\n测试不同模块的日志记录:")
    test_sensor_publisher()
    test_sensor_subscriber()
    
    # 测试自定义配置
    test_custom_config()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("查看 logs/ 目录下的日志文件")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())