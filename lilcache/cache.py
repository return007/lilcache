"""
Everything important goes here
"""

import os
import socket
import pickle

from .util import generate_cache_name, default_root


STATE = dict()
BUFFER_SIZE = 2048
ENCODING = "utf-8"
DELIMITER = b"<<->>"
END_LIMIT = b"<<=>>"


def _handler(conn, cache_path, snapshot, expires):
    pass


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
    cache = dict()

    mgr = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    mgr.bind(sock_path)
    mgr.listen()

    while True:
        conn, addr = mgr.accept()
        command = conn.recv(BUFFER_SIZE)
        packet = command
        while not is_last(command):
            command = conn.recv(BUFFER_SIZE)
            packet += command
        args = decode_payload(packet)
        if args[0] == b'GET':
            key = args[1].decode(ENCODING)
            value = cache.get(key)
            payload = create_payload(b"RES", BUFFER_SIZE, value)
        elif args[0] == b'SET':
            key = args[1].decode(ENCODING)
            value = args[2]
            cache[key] = value
            payload = create_payload(b"RES", BUFFER_SIZE, b'OK')
        elif args[0] == 'POP':
            key = args[1].decode(ENCODING)
            value = cache.pop(key)
            payload = create_payload(b"RES", BUFFER_SIZE, value)
        else:
            print("Invalid operation")
            payload = []
        for p in payload:
            conn.send(p)


def init(
    cache_name=None,
    root=None,
    snapshot=None,
    expires=None,
    poolsize=10
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

    import threading
    mgr = threading.Thread(target=manager,
                           args=(sock_path, cache_path, snapshot, expires, poolsize))
    mgr.start()
    # manager(sock_path, cache_path, snapshot, expires, poolsize)
    return


def establish_connection():
    """
    This is a poor implementation.

    We should try to reuse connections (from the connection pool)
    """
    sock_path = STATE["sock_path"]
    if os.path.exists(sock_path):
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.connect(sock_path)
        return conn


def create_payload(operation, packet_size, *args):
    contents = DELIMITER.join(args)
    packet = operation + DELIMITER + contents + END_LIMIT
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

    if args[0] == b'RES':
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
    print(response)


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
    if args[0] == b'RES':
        return pickle.loads(args[1])
    else:
        print("Some error occurred!")
        print(args)


def destroy():
    sock_path = STATE["sock_path"]
    os.unlink(sock_path)
