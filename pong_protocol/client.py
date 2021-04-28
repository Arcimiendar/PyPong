import threading

from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
from twisted.internet.protocol import Factory

from pong_protocol.protocol import PongProtocol
from main import main
from constants import PORT


def get_protocol_client(ipv4_address):
    class ProtocolGotten:
        def __init__(self):
            self.already_gotten = False

        def __call__(self, p: PongProtocol):
            if self.already_gotten:
                p.transport.loseConnection()
            else:
                self.already_gotten = True
                threading.Thread(target=main, args=(p,), name='game_thread').start()

    point = TCP4ClientEndpoint(reactor, ipv4_address, PORT)
    d: Factory = connectProtocol(point, PongProtocol())
    d.addCallback(ProtocolGotten())
    reactor.run()
