import threading

from twisted.internet import reactor
from pong_protocol.client import get_protocol_client


if __name__ == '__main__':
    get_protocol_client('localhost')
