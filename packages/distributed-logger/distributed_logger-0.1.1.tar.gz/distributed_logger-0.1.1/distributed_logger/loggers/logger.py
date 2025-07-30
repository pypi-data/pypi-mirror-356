from abc import ABC, abstractmethod
from distributed_logger.models.log import LogInfo
from distributed_logger.models.config import Config, KafkaConfig, SimpleConfig
from kafka import KafkaProducer

class Logger(ABC):
     """
          This class is a blueprint and has two major functions:
          - Establising connection
          - Sending Information
     """
     @abstractmethod
     def connect(self):
          raise NotImplementedError("connect must be implemented")
     
     @abstractmethod
     def publish(self, log_info: LogInfo):
          raise NotImplementedError("publish function must be impemented")
     


class KafkaLogger(Logger):
     def __init__(self, config: KafkaConfig) -> None:
          super().__init__()
          self.config = config
          self.producer = None
          self.connect()
     
     def connect(self):
          if not isinstance(self.config, KafkaConfig):
               raise TypeError("KafkaLogger requires a KafkaConfig instance")
          try:
               self.producer = KafkaProducer(
                    bootstrap_servers=self.config.bootstrap_servers,
                    client_id=self.config.client_id,
                    value_serializer=lambda v: v.encode('utf-8')
               )
               print("CONNECTION ESTABLISHED:::: KAFKA")
          except Exception as e:
               print(f"Failed to connect to Kafka: {e}")
               self.producer = None
     
     def publish(self, log_info: LogInfo):
          if not self.producer:
               print("Kafka producer not connected.")
               return
          try:
               topic = self.config.topic
               self.producer.send(topic, log_info.to_json())
               self.producer.flush()
               print("PUBLISHED:::: KAFKA", log_info.to_json())
          except Exception as e:
               print(f"Failed to publish to Kafka: {e}")


class SimpleLogger(Logger):

     def __init__(self, config: Config) -> None:
          self.config = config
          self.connect()

     def connect(self):
          if not isinstance(self.config, SimpleConfig):
               raise TypeError("SimpleLogger requires a SimpleConfig instance")
          print("CONNECTION ESTABLISHED:::: SIMPLE")

          # TODO: Implement connection to RabbitMQ

     def publish(self, log_info: LogInfo):
          if not isinstance(self.config, SimpleConfig):
               raise TypeError("SimpleLogger requires a SimpleConfig instance")
          
          # TODO: Implement publishing to RabbitMQ
          print("PUBLISHING:::: SIMPLE", log_info.to_json())
