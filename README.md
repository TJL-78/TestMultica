# TestMultica - 基于 Fast DDS 的传感器数据发布订阅系统

## 1. 项目概述和简介

TestMultica 是一个基于 Fast DDS (eProsima Fast DDS) 的传感器数据发布订阅系统演示项目。该项目展示了如何使用 DDS (Data Distribution Service) 中间件在分布式系统中实现实时数据通信。

### 主要特性
- **实时数据分发**: 使用 DDS 标准实现高效、可靠的数据通信
- **发布订阅模式**: 支持一对多、多对多的数据分发
- **类型安全**: 使用 IDL (Interface Definition Language) 定义数据类型
- **灵活的日志系统**: 内置多级别、可配置的日志工具
- **Python 实现**: 使用 Fast DDS Python bindings 实现

### 应用场景
- 物联网传感器数据采集和分发
- 工业自动化系统监控
- 分布式系统数据交换
- 实时数据处理和分析

## 2. 系统架构图（文字描述）

```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  SensorData     │     │  SensorData     │
│  Publisher      │────▶│  Subscriber     │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
         │                       │
         │  DDS 通信层           │
         │  (Fast DDS)           │
         ▼                       ▼
┌─────────────────────────────────────────┐
│                                         │
│           DDS 全局数据空间              │
│                                         │
│  ┌─────────────┐    ┌─────────────┐    │
│  │   Topic:    │    │   Topic:    │    │
│  │SensorData   │    │SensorData   │    │
│  │  Topic      │    │  Topic      │    │
│  └─────────────┘    └─────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

### 架构组件说明
1. **发布者 (Publisher)**: 生成传感器数据并发布到 DDS 全局数据空间
2. **订阅者 (Subscriber)**: 订阅传感器数据并接收处理
3. **DDS 中间件 (Fast DDS)**: 提供数据分发服务，管理主题和数据类型
4. **数据类型定义 (IDL)**: 使用 IDL 定义传感器数据结构，确保类型安全

## 3. 快速开始指南

### 环境要求
- Ubuntu 20.04 或更高版本
- Python 3.8+
- 至少 4GB 内存
- 2GB 可用磁盘空间

### 快速运行
```bash
# 终端1 - 启动发布者
python3 SensorDataPublisher.py 1.0 5

# 终端2 - 启动订阅者
python3 SensorDataSubscriber.py
```

## 4. 详细安装步骤

### 4.1 安装系统依赖
```bash
sudo apt update
sudo apt install -y cmake g++ python3-pip python3-dev wget git \
    libasio-dev libtinyxml2-dev libssl-dev swig default-jre gradle
```

### 4.2 安装 Fast DDS 核心组件
```bash
# 创建工作空间
mkdir -p ~/fastdds_ws/src && cd ~/fastdds_ws

# 安装 Fast CDR
wget https://github.com/eProsima/Fast-CDR/archive/refs/tags/v2.2.0.tar.gz -O fastcdr-2.2.0.tar.gz
tar -xzf fastcdr-2.2.0.tar.gz
mv Fast-CDR-2.2.0 Fast-CDR
mkdir Fast-CDR/build && cd Fast-CDR/build
cmake .. && make -j$(nproc) && sudo make install && sudo ldconfig
cd ../..

# 安装 Fast DDS
wget https://github.com/eProsima/Fast-DDS/archive/refs/tags/v2.14.0.tar.gz -O fastdds-2.14.0.tar.gz
tar -xzf fastdds-2.14.0.tar.gz
mv Fast-DDS-2.14.0 Fast-DDS
mkdir Fast-DDS/build && cd Fast-DDS/build
cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_CXX_FLAGS="-Werror" ..
make -j$(nproc) && sudo make install && sudo ldconfig
cd ../..
```

### 4.3 安装 Fast DDS-Gen
```bash
wget https://github.com/eProsima/fastddsgen/archive/refs/tags/v3.1.0.tar.gz -O fastddsgen-3.1.0.tar.gz
tar -xzf fastddsgen-3.1.0.tar.gz
mv fastddsgen-3.1.0 fastddsgen
cd fastddsgen && ./gradlew assemble
export PATH=$PATH:~/fastdds_ws/fastddsgen/scripts
cd ..
```

### 4.4 安装 Fast DDS Python Bindings
```bash
mkdir -p ~/fastdds_python_ws/src
cd ~/fastdds_python_ws
git clone https://github.com/eProsima/Fast-DDS-python.git src/Fast-DDS-python
colcon build --packages-select fastdds_python
export PYTHONPATH=$PYTHONPATH:~/fastdds_python_ws/install/fastdds_python/lib/python3.10/site-packages
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/fastdds_python_ws/install/fastdds_python/lib
cd ..
```

### 4.5 配置环境变量
将以下内容添加到 `~/.bashrc`:
```bash
export PATH=$PATH:~/fastdds_ws/fastddsgen/scripts
export PYTHONPATH=$PYTHONPATH:~/fastdds_python_ws/install/fastdds_python/lib/python3.10/site-packages
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/fastdds_python_ws/install/fastdds_python/lib:/usr/local/lib
```

### 4.6 生成 Python 类型支持
```bash
cd TestMultica
fastddsgen -python SensorData.idl
```

## 5. 使用方法

### 5.1 发布者 (Publisher)
```bash
# 基本用法
python3 SensorDataPublisher.py

# 带参数运行
python3 SensorDataPublisher.py 0.5 20    # 每0.5秒发布，共20条数据
python3 SensorDataPublisher.py 2.0 100   # 每2秒发布，共100条数据
```

**参数说明:**
- `interval`: 发布间隔（秒），默认 1.0
- `num_samples`: 发布数据数量，默认 10

### 5.2 订阅者 (Subscriber)
```bash
# 基本用法
python3 SensorDataSubscriber.py

# 停止订阅者: 按 Ctrl+C
```

### 5.3 多实例运行
```bash
# 多个订阅者
# 终端1: python3 SensorDataSubscriber.py
# 终端2: python3 SensorDataSubscriber.py
# 终端3: python3 SensorDataPublisher.py

# 多个发布者
# 终端1: python3 SensorDataPublisher.py
# 终端2: python3 SensorDataPublisher.py
# 终端3: python3 SensorDataSubscriber.py
```

## 6. 日志系统说明

### 6.1 快速使用
```python
from utils import get_logger

logger = get_logger('my_module')
logger.info("程序启动")
logger.warning("警告信息")
logger.error("错误信息")
```

### 6.2 自定义配置
```python
from utils import get_logger, LoggerConfig

config = LoggerConfig(
    level='DEBUG',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    console=True,
    file=True,
    file_path='logs/myapp.log'
)

logger = get_logger('custom_module', config=config)
```

### 6.3 测试日志工具
```bash
python3 test_logger.py
python3 log_config_example.py
```

**详细文档:** 查看 [LOGGING_README.md](LOGGING_README.md)

## 7. 项目结构
```
TestMultica/
├── SensorData.idl              # 传感器数据类型定义
├── SensorDataPublisher.py      # 发布者程序
├── SensorDataSubscriber.py     # 订阅者程序
├── utils.py                    # 日志工具模块
├── test_logger.py              # 日志测试脚本
├── log_config_example.py       # 日志配置示例
├── LOGGING_README.md           # 日志工具使用说明
├── README.md                   # 本说明文件
└── logs/                       # 日志文件目录
```

## 8. 配置选项

### 8.1 发布者配置
```bash
python3 SensorDataPublisher.py [interval] [num_samples]
```

### 8.2 日志系统配置
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| level | str/int | INFO | 日志级别 |
| format | str | '%(asctime)s - %(name)s - %(levelname)s - %(message)s' | 日志格式 |
| console | bool | True | 控制台输出 |
| file | bool | False | 文件输出 |
| file_path | str | 'logs/app.log' | 日志文件路径 |

### 8.3 数据类型配置
```idl
module sensor {
    struct SensorData {
        @key unsigned long sensor_id;
        double temperature;
        unsigned long timestamp_sec;
        unsigned long timestamp_nanosec;
    };
};
```

## 9. 故障排除

### 常见问题
1. **无法导入 Fast DDS 模块**
   ```bash
   # 检查环境变量
   echo $PYTHONPATH
   echo $LD_LIBRARY_PATH
   
   # 重新生成类型支持
   fastddsgen -python SensorData.idl
   ```

2. **发布者和订阅者无法连接**
   ```bash
   # 检查 Fast DDS 安装
   ldconfig -p | grep fastdds
   
   # 检查防火墙设置
   sudo ufw allow 7400:7500/tcp
   ```

3. **权限问题**
   ```bash
   chmod 755 TestMultica
   ```

## 10. 贡献指南

### 开发流程
1. 创建功能分支: `git checkout -b feature/new-feature`
2. 实现功能并添加测试
3. 提交更改: `git commit -m "feat(scope): description"`
4. 创建 Pull Request

### 代码规范
- 使用 Black 代码格式化
- 遵循 PEP 8 规范
- 使用类型注解
- 添加适当的注释

## 11. 许可证信息

### 项目许可证
TestMultica 采用 MIT 许可证。

### 第三方依赖许可证
- Fast DDS: Apache License 2.0
- Fast CDR: Apache License 2.0
- Fast DDS-Gen: Apache License 2.0
- Fast DDS Python Bindings: Apache License 2.0

## 12. 参考资料
- [Fast DDS 官方文档](https://fast-dds.docs.eprosima.com)
- [Fast DDS Python Bindings](https://github.com/eProsima/Fast-DDS-python)
- [DDS 标准规范](https://www.omg.org/spec/DDS)

---

**最后更新**: 2024年1月15日  
**版本**: 1.0.0  
**作者**: TestMultica 开发团队