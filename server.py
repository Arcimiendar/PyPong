import threading

from twisted.internet import reactor
from pong_protocol.server import get_protocol_server


if __name__ == '__main__':
    get_protocol_server()
