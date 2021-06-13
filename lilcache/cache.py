"""
Everything important goes here
"""

import os
import socket

from .util import generate_cache_name, default_root


STATE = dict()


def _handler(conn, cache_path, snapshot, expires):
    pass
    

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
        print("A new connection: %s %s" % (conn, addr))
        operation = conn.recv(1024)
        """
        while True:
            data = conn.recv(1024)
            if not data:
                break
            operation += data
        """
        print(operation)
        conn.send(b'OK')


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
    sock_path = STATE["sock_path"]
    if os.path.exists(sock_path):
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.connect(sock_path)
        return conn


def get(key):
    conn = establish_connection()
    conn.send(("GET %s" % key).encode("utf-8"))
    response = conn.recv(1024)
    
    return None


def set(key, value):
    pass


def pop(key):
    pass
