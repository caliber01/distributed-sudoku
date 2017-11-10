"""
Module to abstract networking operations, data representation
Message is as tring of format {length_of_message}SEPARATOR{message_type}SEPARATOR{}
"""
import common.protocol as protocol
import json


RECV_BUFFER_BYTES = 1024


def request(sock, request_type, **kargs):
    """
    :param sock: socket to use for connection
    :param request_type: constant from common.protocol
    :param kargs: all other parameters are must be named, they are gathered and converted to JSON
    :return: response as dictionary
    """
    body = json.dumps(kargs)
    # TODO
    msg = protocol.MSG_SEP.join()
    sock.sendall(msg)
    return _recv(sock)


def _recv(sock):
    resp = sock.recv(RECV_BUFFER_BYTES)
    raw_size = resp.split(protocol.MSG_SEP)[0]
    msg_size_bytes = int(raw_size)
    if msg_size_bytes > RECV_BUFFER_BYTES:
        received_bytes = len(resp)
        while received_bytes < msg_size_bytes:
            chunk = sock.recv(min(RECV_BUFFER_BYTES, msg_size_bytes - received_bytes))
            resp += chunk
            received_bytes += len(resp)
    _, data = resp.split(protocol.MSG_SEP)
    return json.loads(data)

