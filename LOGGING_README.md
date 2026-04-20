# 日志工具使用说明

## 概述

本日志工具提供了灵活的日志记录功能，支持不同日志级别、控制台输出和文件输出，以及日志格式自定义。

## 主要特性

1. **多级别日志**: DEBUG, INFO, WARNING, ERROR, CRITICAL
2. **双输出**: 支持控制台和文件同时输出
3. **格式自定义**: 可自定义日志格式和日期时间格式
4. **文件轮转**: 支持日志文件大小限制和备份
5. **模块化**: 不同模块可以使用不同的日志记录器

## 快速开始

### 基本使用

```python
from utils import get_logger

# 获取默认配置的日志记录器
logger = get_logger('my_module')

# 记录不同级别的日志
logger.debug("调试信息")
logger.info("程序启动")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

### 自定义配置

```python
from utils import get_logger, LoggerConfig

# 创建自定义配置
config = LoggerConfig(
    level='DEBUG',  # 日志级别
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    date_format='%H:%M:%S',
    console=True,    # 启用控制台输出
    file=True,       # 启用文件输出
    file_path='logs/app.log',
    max_bytes=10485760,  # 10MB
    backup_count=5
)

# 使用自定义配置获取日志记录器
logger = get_logger('custom_module', config=config)
```

### 便捷函数

```python
from utils import get_logger

# 直接通过参数配置
logger = get_logger(
    'myapp',
    level='INFO',
    console=True,
    file=True,
    file_path='logs/myapp.log'
)
```

## 在现有项目中使用

### SensorDataPublisher.py 示例

```python
from utils import get_logger

class SensorDataWriter:
    def __init__(self):
        self.logger = get_logger('publisher.writer')
        
    def write(self, sensor_id, temperature):
        # ... 业务逻辑 ...
        self.logger.info(f"发布传感器数据 [ID: {sensor_id}, 温度: {temperature:.2f}°C]")
```

### SensorDataSubscriber.py 示例

```python
from utils import get_logger

class ReaderListener(fastdds.DataReaderListener):
    def __init__(self):
        self.logger = get_logger('subscriber.listener')
        
    def on_data_available(self, reader):
        # ... 业务逻辑 ...
        self.logger.info(f"收到传感器数据 [ID: {data.sensor_id()}, 温度: {data.temperature():.2f}°C]")
```

## 配置参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| level | str/int | INFO | 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| format | str | '%(asctime)s - %(name)s - %(levelname)s - %(message)s' | 日志格式 |
| date_format | str | '%Y-%m-%d %H:%M:%S' | 日期时间格式 |
| console | bool | True | 是否启用控制台输出 |
| file | bool | False | 是否启用文件输出 |
| file_path | str | 'logs/app.log' | 日志文件路径 |
| file_mode | str | 'a' | 文件打开模式 ('a'追加, 'w'覆盖) |
| max_bytes | int | 10485760 | 日志文件最大字节数(10MB) |
| backup_count | int | 5 | 保留的备份文件数量 |

## 日志格式变量

| 变量 | 说明 |
|------|------|
| %(asctime)s | 日志记录时间 |
| %(name)s | 日志记录器名称 |
| %(levelname)s | 日志级别 |
| %(message)s | 日志消息 |
| %(pathname)s | 调用日志记录函数的源文件路径 |
| %(filename)s | 文件名 |
| %(module)s | 模块名 |
| %(funcName)s | 函数名 |
| %(lineno)d | 行号 |
| %(process)d | 进程ID |
| %(thread)d | 线程ID |

## 示例

### 运行测试脚本

```bash
python test_logger.py
```

### 运行修改后的发布器

```bash
python SensorDataPublisher.py
```

### 运行修改后的订阅器

```bash
python SensorDataSubscriber.py
```

## 高级用法

### 异常记录

```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError as e:
    logger.error("发生除零错误", exc_info=True)
    # 或者使用便捷方法
    logger.exception("发生除零错误: %s", str(e))
```

### 带参数的日志

```python
temperature = 25.5
humidity = 60.2
logger.info("传感器数据 - 温度: %.1f°C, 湿度: %.1f%%", temperature, humidity)
```

### 设置全局默认配置

```python
from utils import LogManager, LoggerConfig

# 设置全局默认配置
default_config = LoggerConfig(
    level='INFO',
    console=True,
    file=True,
    file_path='logs/default.log'
)
LogManager.set_default_config(default_config)
```

## 文件结构

```
TestMultica/
├── utils.py              # 日志工具主文件
├── test_logger.py        # 测试脚本
├── SensorDataPublisher.py # 使用日志的发布器
├── SensorDataSubscriber.py # 使用日志的订阅器
└── logs/                 # 日志文件目录
    ├── app.log          # 默认日志文件
    ├── example.log      # 示例日志文件
    └── test.log         # 测试日志文件
```

## 注意事项

1. 日志目录会自动创建，无需手动创建
2. 文件轮转功能在文件大小超过 `max_bytes` 时自动触发
3. 不同模块使用不同的日志记录器名称，便于过滤和查找
4. 生产环境中建议将日志级别设置为 INFO 或 WARNING
5. 调试时可以将日志级别设置为 DEBUG 查看更多信息