"""
lil utilities for lilcache
"""

import os


def generate_cache_name():
    """
    Cache name generating algorithm
    """
    return "process_PID"

def default_root():
    """
    Default root for the lilcaches.
    """
    home_dir = os.path.expanduser("~")
    path = os.path.join(home_dir, ".lilcache")
    if not os.path.exists(path):
        os.mkdir(path)
    return path
