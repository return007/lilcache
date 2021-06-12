# Design

## Requirements

1. Multi process and thread safe cache

```
# Process1
import lilcache
lilcache.set('a', 'b')

# Process2
import lilcache
lilcache.get('a')

# Process3
import lilcache
lilcache.pop('a')
```

2. Named cache

```
import lilcache
lilcache.init('foo_cache')
lilcache.set('a', 'b')
```

3. Snapshot at regular intervals

```
import lilcache
lilcache.init('foo_cache', snapshot='120s')
lilcache.set('a', 'b')
```

4. Delete cache

```
import lilcache
lilcache.set('a', 'b')
lilcache.purge()
```

5. Expire cache

```
import lilcache
lilcache.init('foo_cache', expires='1d')
lilcache.set('a', 'b')
```

6. RESTful

```
import lilcache
lilcache.init('foo_cache')
lilcache.start(host='0.0.0.0', port=5001)  # Blocking call
```

```
$ curl localhost:5001/get?key=a
'b'
$ curl localhost:5001/set?key=a&value=b
OK
```

7. Cache path

```
import lilcache
lilcache.init('foo_cache', root='/home/user/secured-directory')
lilcache.set('password', 'hello123')
```

8. Logging

```
import lilcache
lilcache.init(loglevel='DEBUG')     # log file will be stored under root
lilcache.set('a', 'b')
```

## Inter process communication approaches

### IPC with FIFO
1. P1 creates FIFO (named pipe)
2. Other processes communicate to P1 about operations (get/set/delete)
3. P1 acts as master process and manages the state in memory (but what if it exists, electing new master?)
4. P1 will be responsible for creating cache snapshots

#### What if P1 (manager process) exists
1. Need election algorithm (think more!)
2. To retain the state of cache in newly elected manager (P2), we need to maintain list of set/delete operations
3. This list of operations will be optimized (sort of tree shaking) time to time


### IPC with sockets
1. P1 creates local socket
2. Other processes communicate to P1 about operations (get/set/delete)
3. P1 acts as master process and manages the state in memory (but what if it exists, electing new master?)
4. P1 will be responsible for creating snapshots

#### What if P1 (manager process) exists
1. Need election algorithm (think more!)
2. To retain the state of cache in newly elected manager (P2), we need to maintain list of set/delete operations
3. This list of operations will be optimized (sort of tree shaking) time to time


### "Incoordinated" cache | No IPC
1. No concept of master process
2. Each process will read from disk (get/set/delete)
3. Each process can have a local in-memory cache (but problem of synchronization)
