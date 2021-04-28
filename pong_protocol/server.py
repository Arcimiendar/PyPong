from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Factory

from pong_protocol.protocol import PongFactory
from constants import PORT


def get_protocol_server():
    point = TCP4ServerEndpoint(reactor, PORT)
    d: Factory = PongFactory()

    point.listen(d)
    reactor.run()
