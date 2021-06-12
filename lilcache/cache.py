"""
Everything important goes here
"""

import os

from .util import generate_cache_name, default_root


def init(
    cache_name=None,
    root=None,
    snapshot=None,
    expires=None,
):
    if not cache_name:
        cache_name = generate_cache_name()
    cache_name = "%s.lc" % cache_name
    if not root:
        root = default_root()
    cache_path = os.path.join(root, cache_name)
    return cache_path
