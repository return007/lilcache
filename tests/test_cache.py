"""
Unittests for lilcache

"""

import pytest
import lilcache


def setup_module(module=None):
    lilcache.init()


def teardown_module(module=None):
    print("I am being called")
    lilcache.destroy()


def test_set_str():
    response = lilcache.set('foo', 'bar')
    assert response == True


def test_set_int():
    response = lilcache.set('num1', 1)
    assert response == True


def test_set_float():
    response = lilcache.set('num2', 2.01)
    assert response == True
