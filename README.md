# SensorData DDS 示例程序

基于Fast DDS (eProsima Fast DDS) 的发布订阅示例程序，用于演示DDS数据分发服务。

## 目录结构

```
TestMultica/
├── SensorData.idl              # 传感器数据类型定义
├── SensorDataPublisher.py      # 发布者程序
├── SensorDataSubscriber.py     # 订阅者程序
├── utils.py                    # 日志工具模块
├── test_logger.py              # 日志测试脚本
├── log_config_example.py       # 日志配置示例
├── LOGGING_README.md           # 日志工具使用说明
└── README.md                   # 本说明文件
```

## 依赖安装

### 1. 安装系统依赖 (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y \
    cmake \
    g++ \
    python3-pip \
    python3-dev \
    wget \
    git \
    libasio-dev \
    libtinyxml2-dev \
    libssl-dev \
    swig
```

### 2. 安装Fast DDS

Fast DDS需要从源码编译安装：

```bash
mkdir -p ~/fastdds_ws/src
cd ~/fastdds_ws
wget https://github.com/eProsima/Fast-DDS/archive/refs/tags/v2.14.0.tar.gz -O fastdds-2.14.0.tar.gz
tar -xzf fastdds-2.14.0.tar.gz
mv Fast-DDS-2.14.0 Fast-DDS
mkdir build && cd build
cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_CXX_FLAGS="-Werror" ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 3. 安装Fast CDR (必须)

```bash
cd ~/fastdds_ws/src
wget https://github.com/eProsima/Fast-CDR/archive/refs/tags/v2.2.0.tar.gz -O fastcdr-2.2.0.tar.gz
tar -xzf fastcdr-2.2.0.tar.gz
mv Fast-CDR-2.2.0 Fast-CDR
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

### 4. 安装Fast DDS-Gen

```bash
cd ~/fastdds_ws
wget https://github.com/eProsima/fastddsgen/archive/refs/tags/v3.1.0.tar.gz -O fastddsgen-3.1.0.tar.gz
tar -xzf fastddsgen-3.1.0.tar.gz
mv fastddsgen-3.1.0 fastddsgen
cd fastddsgen
./gradlew assemble
export PATH=$PATH:~/fastdds_ws/fastddsgen/scripts
```

### 5. 安装Fast DDS Python Bindings

```bash
mkdir -p ~/fastdds_python_ws/src
cd ~/fastdds_python_ws
git clone https://github.com/eProsima/Fast-DDS-python.git src/Fast-DDS-python
colcon build --packages-select fastdds_python
export PYTHONPATH=$PYTHONPATH:~/fastdds_python_ws/install/fastdds_python/lib/python3.10/site-packages
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/fastdds_python_ws/install/fastdds_python/lib
```

### 6. 生成Python类型支持

```bash
cd TestMultica
fastddsgen -python SensorData.idl
```

## 运行示例

### 终端1 - 运行Publisher:

```bash
cd TestMultica
export PYTHONPATH=$PYTHONPATH:$(pwd)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
python3 SensorDataPublisher.py 1.0 10
```

### 终端2 - 运行Subscriber:

```bash
cd TestMultica
export PYTHONPATH=$PYTHONPATH:$(pwd)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
python3 SensorDataSubscriber.py
```

## 日志工具

项目包含一个灵活的日志工具，支持多级别日志、控制台和文件输出、格式自定义等功能。

### 快速使用

```python
from utils import get_logger

logger = get_logger('my_module')
logger.info("程序启动")
logger.warning("警告信息")
```

### 详细说明

查看 [LOGGING_README.md](LOGGING_README.md) 获取完整的使用说明和配置示例。

### 测试日志工具

```bash
python3 test_logger.py
python3 log_config_example.py
```

## 数据类型

| 字段 | 类型 | 描述 |
|------|------|------|
| sensor_id | unsigned long | 传感器ID |
| temperature | double | 温度值(摄氏度) |
| timestamp_sec | unsigned long | 时间戳(秒) |
| timestamp_nanosec | unsigned long | 时间戳(纳秒) |

## 参考资料

- [Fast DDS官方文档](https://fast-dds.docs.eprosima.com)
- [Fast DDS Python Bindings](https://github.com/eProsima/Fast-DDS-python)