import threading
from typing import Tuple
from main import main
from pong_protocol.event import Event

from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver


class PongProtocol(LineReceiver):
    def __init__(self, is_server: bool):
        self.events = []
        self.is_server = is_server
        self.main_thread = None
        self.lock = threading.Lock()
        super(PongProtocol, self).__init__()

    def connectionMade(self):
        if not self.main_thread:
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
        return PongProtocol(is_server=True)
