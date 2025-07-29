from enum import Enum
from typing import Sequence
from entity import Entity



class Payload(Entity):

    def __init__(
            self,
            deviceId: str,
            temperature: float,
            timestamp: str):
        self.deviceId = deviceId
        self.temperature = temperature
        self.timestamp = timestamp



