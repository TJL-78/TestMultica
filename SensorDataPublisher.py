"""
SensorData Publisher
使用Fast DDS Python bindings发布传感器数据
"""

import time
import sys
import random
from threading import Condition

import fastdds
import SensorData


class WriterListener(fastdds.DataWriterListener):
    def __init__(self, writer):
        self._writer = writer
        super().__init__()

    def on_publication_matched(self, datawriter, info):
        if 0 < info.current_count_change:
            print(f"Publisher matched subscriber {info.last_subscription_handle}")
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader += 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()
        else:
            print(f"Publisher unmatched subscriber {info.last_subscription_handle}")
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader -= 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()


class SensorDataWriter:
    def __init__(self):
        self._matched_reader = 0
        self._cvDiscovery = Condition()
        self.sample_id = 1
        self.sensor_id = 1

        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant_qos = fastdds.DomainParticipantQos()
        factory.get_default_participant_qos(self.participant_qos)
        self.participant = factory.create_participant(0, self.participant_qos)

        self.topic_data_type = SensorData.SensorDataPubSubType()
        self.topic_data_type.set_name("SensorData")
        self.type_support = fastdds.TypeSupport(self.topic_data_type)
        self.participant.register_type(self.type_support)

        self.topic_qos = fastdds.TopicQos()
        self.participant.get_default_topic_qos(self.topic_qos)
        self.topic = self.participant.create_topic(
            "SensorDataTopic", self.topic_data_type.get_name(), self.topic_qos)

        self.publisher_qos = fastdds.PublisherQos()
        self.participant.get_default_publisher_qos(self.publisher_qos)
        self.publisher = self.participant.create_publisher(self.publisher_qos)

        self.listener = WriterListener(self)
        self.writer_qos = fastdds.DataWriterQos()
        self.publisher.get_default_datawriter_qos(self.writer_qos)
        self.writer = self.publisher.create_datawriter(
            self.topic, self.writer_qos, self.listener)

    def write(self, sensor_id, temperature):
        data = SensorData.SensorData()
        data.sensor_id(sensor_id)
        data.temperature(temperature)

        current_time = time.time()
        data.timestamp_sec(int(current_time))
        data.timestamp_nanosec(int((current_time - int(current_time)) * 1e9))

        self.writer.write(data)
        print(f"发布传感器数据 [ID: {sensor_id}, 温度: {temperature:.2f}°C, 时间戳: {data.timestamp_sec()}.{data.timestamp_nanosec()}]")

    def wait_discovery(self):
        self._cvDiscovery.acquire()
        print("等待Subscriber发现...")
        self._cvDiscovery.wait_for(lambda: self._matched_reader != 0)
        self._cvDiscovery.release()
        print("发现完成!")

    def run(self, interval=1.0, num_samples=10):
        self.wait_discovery()
        for x in range(num_samples):
            time.sleep(interval)
            temperature = 20.0 + random.uniform(-5.0, 15.0)
            self.write(self.sensor_id, temperature)
            self.sample_id += 1

    def delete(self):
        self.participant.delete_contained_entities()
        factory = fastdds.DomainParticipantFactory.get_instance()
        factory.delete_participant(self.participant)


def main():
    print("SensorData Publisher")
    print("=" * 40)

    interval = 1.0
    num_samples = 10

    if len(sys.argv) > 1:
        try:
            interval = float(sys.argv[1])
        except ValueError:
            pass

    if len(sys.argv) > 2:
        try:
            num_samples = int(sys.argv[2])
        except ValueError:
            pass

    writer = SensorDataWriter()
    writer.run(interval, num_samples)
    writer.delete()

    return 0


if __name__ == "__main__":
    sys.exit(main())