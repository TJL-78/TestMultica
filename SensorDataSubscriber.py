"""
SensorData Subscriber
使用Fast DDS Python bindings订阅传感器数据
"""

import signal
import sys

import fastdds
import SensorData


class ReaderListener(fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()

    def on_subscription_matched(self, datareader, info):
        if 0 < info.current_count_change:
            print(f"Subscriber matched publisher {info.last_publication_handle}")
        else:
            print(f"Subscriber unmatched publisher {info.last_publication_handle}")

    def on_data_available(self, reader):
        info = fastdds.SampleInfo()
        data = SensorData.SensorData()
        reader.take_next_sample(data, info)

        print(f"收到传感器数据 [ID: {data.sensor_id()}, 温度: {data.temperature():.2f}°C, 时间戳: {data.timestamp_sec()}.{data.timestamp_nanosec()}]")


class SensorDataReader:
    def __init__(self):
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

        self.subscriber_qos = fastdds.SubscriberQos()
        self.participant.get_default_subscriber_qos(self.subscriber_qos)
        self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

        self.listener = ReaderListener()
        self.reader_qos = fastdds.DataReaderQos()
        self.subscriber.get_default_datareader_qos(self.reader_qos)
        self.reader = self.subscriber.create_datareader(
            self.topic, self.reader_qos, self.listener)

    def delete(self):
        self.participant.delete_contained_entities()
        factory = fastdds.DomainParticipantFactory.get_instance()
        factory.delete_participant(self.participant)

    def run(self):
        def signal_handler(sig, frame):
            print("\n收到中断信号，停止订阅")
            self.delete()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        print("等待数据... (按Ctrl+C停止)")
        signal.pause()


def main():
    print("SensorData Subscriber")
    print("=" * 40)

    reader = SensorDataReader()
    reader.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())