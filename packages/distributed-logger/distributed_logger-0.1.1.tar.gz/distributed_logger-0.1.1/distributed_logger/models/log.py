import json
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class LogInfo:
    ip_address: Optional[str]
    user_id:  Optional[str]
    request_time:  Optional[str]
    action: Optional[str]
    request_data:  Optional[Dict]

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
