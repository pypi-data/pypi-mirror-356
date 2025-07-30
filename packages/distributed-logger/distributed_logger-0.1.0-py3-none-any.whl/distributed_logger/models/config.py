from dataclasses import dataclass
from typing import Dict, Optional, List


@dataclass
class Config:
    broker_type: str


@dataclass
class KafkaConfig(Config):
    bootstrap_servers: List[str]
    topic: str
    client_id: Optional[str] = None


@dataclass
class SimpleConfig(Config):
    pass


class ConfigFactory:
    @staticmethod
    def create_config(config_type: str, **kwargs):
        if config_type == "kafka":
            return KafkaConfig(**kwargs)
        elif config_type == "simple":
            return SimpleConfig(**kwargs)
        else:
            raise ValueError(f"Unknown config type: {config_type}")