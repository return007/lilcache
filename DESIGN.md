# Design

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
