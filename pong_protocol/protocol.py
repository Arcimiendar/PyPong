import json
import threading
from typing import Tuple, Union
from dataclasses import dataclass

from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver


@dataclass
class Event:
    type: str
    remote_height: Union[int, None] = None

    def to_line(self):
        return json.dumps({'type': self.type, 'remote_height': self.remote_height}).encode()
    
    @classmethod
    def from_line(cls, line):
        data = json.loads(line)
        return cls(**data)


class PongProtocol(LineReceiver):
    def __init__(self):
        self.events = []
        self.main_thread = None
        self.lock = threading.Lock()
        super(PongProtocol, self).__init__()

    def connectionMade(self):
        if not self.main_thread:
            from main import main
            self.main_thread = threading.Thread(target=main, args=(self,), name='game_thread')
            self.main_thread.start()

    def rawDataReceived(self, data):
        pass
    
    def get_available_events(self):
        with self.lock:
            events, self.events = self.events, []
        return events
        
    def lineReceived(self, line):
        data = Event.from_line(line)
        with self.lock:
            self.events.append(data)


class PongFactory(Factory):
    def buildProtocol(self, addr: Tuple[str, int]) -> Protocol:
        return PongProtocol()
