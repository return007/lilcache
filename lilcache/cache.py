"""
Everything important goes here
"""

import os
import threading
import socket
import pickle

from .util import generate_cache_name, default_root


STATE = dict()
BUFFER_SIZE = 2048
ENCODING = "utf-8"
DELIMITER = b"<<->>"
END_LIMIT = b"<<=>>"
NONE_VALUE = pickle.dumps(None)
RESPONSE_OK = b"OK"
RESPONSE_ERROR = b"ERR"
cache = dict()


def handle_connection(conn, cache_path, snapshot, expires):
    while True:
        command = conn.recv(BUFFER_SIZE)
        packet = command
        while not is_last(command):
            command = conn.recv(BUFFER_SIZE)
            packet += command
        args = decode_payload(packet)
        if args[0] == b'GET':
            key = args[1].decode(ENCODING)
            value = cache.get(key, NONE_VALUE)
            payload = create_payload(RESPONSE_OK, BUFFER_SIZE, value)
        elif args[0] == b'SET':
            key = args[1].decode(ENCODING)
            value = args[2]
            try:
                cache[key] = value
            except Exception as e:
                payload = create_payload(RESPONSE_ERROR, BUFFER_SIZE,
                                            pickle.dumps(e))
            else:
                payload = create_payload(RESPONSE_OK, BUFFER_SIZE)
        elif args[0] == b'POP':
            key = args[1].decode(ENCODING)
            value = cache.pop(key, NONE_VALUE)
            payload = create_payload(RESPONSE_OK, BUFFER_SIZE, value)
        else:
            print("Invalid operation")
            payload = []
        for p in payload:
            conn.send(p)


def is_last(packet):
    return packet.endswith(END_LIMIT)



def manager(sock_path, cache_path, snapshot, expires, poolsize):
    """
    The manager thread.

    poolsize is used to manage the persistent client connections to the
    manager.  If there are more than desired connections, then we kill
    the most infrequently used connections.

    TODO: Later think about snapshot and expires!
    """
    mgr = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    mgr.bind(sock_path)
    mgr.listen()

    connection_pool = []

    while True:
        conn, addr = mgr.accept()
        if len(connection_pool) <= poolsize:
            # Handle it in a thread
            th = threading.Thread(target=handle_connection,
                                  args=(conn, cache_path, snapshot, expires))
            th.setDaemon(True)
            th.start()
            connection_pool.append(th)
            continue
        else:
            raise NotImplemented("poolsize should be equal or more than 'expected' "
                                 "concurrency level")

def init(
    cache_name=None,
    root=None,
    snapshot=None,
    expires=None,
    poolsize=20
):
    if not cache_name:
        cache_name = generate_cache_name()
    if not root:
        root = default_root()

    sock_path = "%s.sock" % os.path.join(root, cache_name)
    cache_path = "%s.lil" % os.path.join(root, cache_name)

    STATE["sock_path"] = sock_path
    STATE["cache_path"] = cache_path

    if os.path.exists(sock_path):
        return

    mgr = threading.Thread(target=manager,
                           args=(sock_path, cache_path, snapshot, expires, poolsize))
    mgr.setDaemon(True)
    mgr.start()


def establish_connection():
    """
    This is a poor implementation.

    We should try to reuse connections (from the connection pool)
    """
    if "connection" in STATE:
        return STATE["connection"]
    sock_path = STATE["sock_path"]
    if os.path.exists(sock_path):
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.connect(sock_path)
        STATE["connection"] = conn
        return conn


def create_payload(operation, packet_size, *args):
    contents = DELIMITER.join(args)
    if contents:
        packet = operation + DELIMITER + contents + END_LIMIT
    else:
        packet = operation + END_LIMIT
    if len(packet) < packet_size:
        yield packet
        return
    # Break the packet into multiple packets for transmission
    for i in range(0, len(packet), packet_size):
        yield packet[i:i+packet_size]


def decode_payload(packet):
    packet = packet.split(END_LIMIT)[0]
    d = packet.split(DELIMITER)
    return d


def get(key):
    conn = establish_connection()
    payload = create_payload(b'GET', BUFFER_SIZE, key.encode(ENCODING))
    for p in payload:
        conn.send(p)
    packet = conn.recv(BUFFER_SIZE)
    response = packet
    while not is_last(packet):
        packet = conn.recv(BUFFER_SIZE)
        response += packet

    args = decode_payload(response)

    if args[0] == RESPONSE_OK:
        return pickle.loads(args[1])
    else:
        print("Some error occurred!")
        print(args)


def set(key, value):
    conn = establish_connection()
    payload = create_payload(b'SET', BUFFER_SIZE, key.encode(ENCODING), pickle.dumps(value))
    for p in payload:
        conn.send(p)
    packet = conn.recv(BUFFER_SIZE)
    response = packet
    while not is_last(packet):
        packet = conn.recv(BUFFER_SIZE)
        response += packet

    args = decode_payload(response)
    if args[0] == RESPONSE_OK:
        return True
    elif args[0] == RESPONSE_ERROR:
        raise pickle.loads(args[1])


def pop(key):
    conn = establish_connection()
    payload = create_payload(b'POP', BUFFER_SIZE, key.encode(ENCODING))
    for p in payload:
        conn.send(p)
    packet = conn.recv(BUFFER_SIZE)
    response = packet
    while not is_last(packet):
        packet = conn.recv(BUFFER_SIZE)
        response += packet

    args = decode_payload(response)
    if args[0] == RESPONSE_OK:
        return pickle.loads(args[1])
    else:
        print("Some error occurred!")
        print(args)


def destroy():
    sock_path = STATE["sock_path"]
    os.remove(sock_path)
