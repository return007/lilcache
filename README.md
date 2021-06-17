# lilcache

[![PyPI version lilcache](https://img.shields.io/pypi/v/lilcache.svg)](https://pypi.python.org/pypi/lilcache/)
[![PyPI license](https://img.shields.io/pypi/l/lilcache.svg)](https://pypi.python.org/pypi/lilcache/)

## Interprocess and thread safe light weight cache

**Note:**
This is under development and has bad performance (concurrency, response time, error prone, etc. you name it!). 
It is not ready for production use.  If you like taking risks, I won't stop you from using it.

## How to

```
$ pip install lilcache

$ python
>>> import lilcache
>>> lilcache.init()
>>> lilcache.set('foo', 'bar')
True
>>> lilcache.get('foo')
'bar'
```

## Benchmarks

### lilcache vs redis

**Note: lilcache was running without connection pool**

For obvious reasons, redis is performing better than lilcache and
the performance gap increases a lot with increasing concurrency.

*Benchmarking tool run on Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz*

```
$ python3 tests/benchmarks/performance.py
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| Cache type   |   Concurrency |   Number of operations (get/set/delete) |   Mean response time (ms) |   Lowest time (ms) |   Highest time (ms) |
+==============+===============+=========================================+===========================+====================+=====================+
| lilcache     |             1 |                                    1000 |                 0.0368855 |          0.0350475 |            0.200033 |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |             1 |                                    1000 |                 0.0323646 |          0.0274181 |            1.01137  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |             5 |                                    1000 |                 0.0754766 |          0.0412464 |            0.260592 |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |             5 |                                    1000 |                 0.0399675 |          0.0283718 |            1.13201  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |            10 |                                    1000 |                 0.185351  |          0.142813  |            0.473261 |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |            10 |                                    1000 |                 0.06568   |          0.0295639 |            1.37901  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |            20 |                                    1000 |                 0.376953  |          0.166655  |            1.16491  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |            20 |                                    1000 |                 0.102541  |          0.0293255 |            1.88661  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
```

### lilcache vs redis

**Note: lilcache was running with connection pool**
High number of threads is performing worse than no threads.
Seems like Python GIL is biting us here.

```
$ python3 tests/benchmarks/performance.py
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| Cache type   |   Concurrency |   Number of operations (get/set/delete) |   Mean response time (ms) |   Lowest time (ms) |   Highest time (ms) |
+==============+===============+=========================================+===========================+====================+=====================+
| lilcache     |             1 |                                    1000 |                 0.0102515 |         0.00786781 |            0.223398 |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |             1 |                                    1000 |                 0.0333166 |         0.0283718  |            1.07622  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |             5 |                                    1000 |                 0.0693438 |         0.0123978  |            0.691175 |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |             5 |                                    1000 |                 0.0532017 |         0.0312328  |            1.34492  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |            10 |                                    1000 |                 0.233874  |         0.0140667  |            2.32434  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |            10 |                                    1000 |                 0.0799031 |         0.0324249  |            2.46119  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| lilcache     |            20 |                                    1000 |                 0.578124  |         0.0114441  |            8.94666  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
| redis        |            20 |                                    1000 |                 0.100958  |         0.0321865  |            4.00949  |
+--------------+---------------+-----------------------------------------+---------------------------+--------------------+---------------------+
```


## Timeline

 - [ ] Write unittests
 - [X] Stress testing
 - [ ] Improve error handling
 - [ ] Extension to current implementation: Implement connection pool and client reuse connections
 - [ ] Implementation 2: Twisted bsaed concurrency
 - [ ] Implementation 3: Incordinated cache (file db + locks for synchronization)
 - [ ] For each implementation, perform benchmark tests and stress testing
 - [X] Release to PyPi (pre-alpha release done)
 - [ ] Implementation 4: Named PIPE based approach and full duplex communication
 - [ ] Add more features (snapshot, Cache expiry, etc.)
 - [ ] Production ready code
 
## Contributing

Contributions are welcome!  For more details, please read the [CONTRIBUTING.md](CONTRIBUTING.md)
