from twisted.internet.endpoints import TCP4ServerEndpoint, connectProtocol
from twisted.internet import reactor
from twisted.internet.protocol import Factory

from pong_protocol.protocol import PongProtocol, PongFactory
from main import main
from constants import PORT


def get_protocol_server():
    point = TCP4ServerEndpoint(reactor, PORT)
    d: Factory = PongFactory()
    # d.addCallback(ProtocolGotten())

    point.listen(d)
    reactor.run()
