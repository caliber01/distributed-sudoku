import common.protocol as protocol
import socket
import time
import multiprocessing as mp
import logging


logger = logging.getLogger(__name__)


def multicast_uri(uri):
    while True:
        logger.info('Multicasting server address')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(str(uri).encode('utf8'), (protocol.MCAST_GRP, protocol.MCAST_PORT))
        time.sleep(5)

def start_broadcasting(uri):
    p = mp.Process(target=multicast_uri, args=(uri,))
    p.start()
