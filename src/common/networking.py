"""
Module to abstract networking operations, data representation
Message is as tring of format {length_of_message}{body}
"""
import common.protocol as protocol
import json


RECV_BUFFER_BYTES = 1024
MSG_SIZE_BYTES = 10


def request(sock, **kargs):
    """
    :param sock: socket to use for connection
    :param request_type: constant from common.protocol
    :param kargs: all other parameters are must be named, they are gathered and converted to JSON
    :return: response as dictionary
    """
    send(sock, **kargs)
    return recv(sock)


def recv(sock):
    raw_size = sock.recv(MSG_SIZE_BYTES)
    msg_size_bytes = int(raw_size)
    resp = ''
    received_bytes = 0
    while received_bytes < msg_size_bytes:
        chunk = sock.recv(min(RECV_BUFFER_BYTES, msg_size_bytes - received_bytes))
        resp += chunk
        received_bytes += len(resp)
    return json.loads(resp)


def send(sock, **kargs):
    body = json.dumps(kargs)
    size = len(body)
    padded_size = str(size).zfill(MSG_SIZE_BYTES)
    sock.sendall(padded_size + body)

