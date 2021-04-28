from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor

from pong_protocol.protocol import PongProtocol
from constants import PORT


def get_protocol_client(ipv4_address):
    point = TCP4ClientEndpoint(reactor, ipv4_address, PORT)
    connectProtocol(point, PongProtocol(is_server=False))
    reactor.run()
