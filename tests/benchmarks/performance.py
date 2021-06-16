"""
Performance testing

Different caches:

 1. lilcache
 2. redis

TODO: Add more cache performance benchmarks!
"""

import time
import tabulate
import subprocess
from statistics import mean, median
from concurrent.futures import ProcessPoolExecutor


def operations(count, seed_val=1):
    """
    Generate ``count`` number of operations.
    """
    from random import choice, seed
    from string import ascii_lowercase, digits
    seed(seed_val)
    chars = ascii_lowercase + digits

    KEY_LENGTH = 10
    VALUE_LENGTH = 20

    op = [
        {
            "type": "GET",
            "params": None
        },
        {
            "type": "SET",
            "params": None
        },
        {
            "type": "POP",
            "params": None
        }
    ]

    keys = [''.join(choice(chars) for _ in range(KEY_LENGTH)) for i in range(count//2)]

    for i in range(count):
        ch = choice(op).copy()
        key = choice(keys)
        if ch["type"] == "GET":
            ch["params"] = (key, )
        elif ch["type"] == "SET":
            value = ''.join(choice(chars) for _ in range(VALUE_LENGTH))
            ch["params"] = (key, value)
        elif ch["type"] == "POP":
            ch["params"] = (key, )
        yield ch


def lilcache_worker(operation):
    # Setup
    import lilcache
    lilcache.init()

    # Actual work
    runtimes = []
    for op in operation:
        if op["type"] == "GET":
            start = time.time()
            lilcache.get(op["params"][0])
            end = time.time()
        elif op["type"] == "SET":
            start = time.time()
            lilcache.set(op["params"][0], op["params"][1])
            end = time.time()
        elif op["type"] == "POP":
            start = time.time()
            lilcache.pop(op["params"][0])
            end = time.time()
        runtimes.append((end-start) * 1e3)  # ms over s

    # Return stats
    return {
        "operations": len(operation),
        "time": sum(runtimes),
        "low": min(runtimes),
        "high": max(runtimes),
        "mean": mean(runtimes),
        "median": median(runtimes)
    }


def combine_stats(stats):
    return {
        "operations": sum(map(lambda x: x["operations"], stats)),
        "time": sum(map(lambda x: x["time"], stats)),
        "low": min(map(lambda x: x["low"], stats)),
        "high": max(map(lambda x: x["high"], stats)),
        "mean": mean(map(lambda x: x["mean"], stats)),
        "median": median(map(lambda x: x["median"], stats))
    }


def test_lilcache(nproc, nop):
    """
    Launch ``nproc`` number of processes (i.e. measure of concurrency).
    """
    import lilcache
    lilcache.init()
    op = list(operations(nop, seed_val=nproc))
    window = nop // nproc
    stats = []
    processes = []
    with ProcessPoolExecutor(nproc) as executor:
        for p in range(nproc):
            processes.append(executor.submit(lilcache_worker, op[window*p:window*(p+1)]))

    for p in processes:
        stats.append(p.result())

    lilcache.destroy()
    return combine_stats(stats)


def redis_worker(operation):
    # Setup
    import redis
    cli = redis.Redis(port=54321)

    # Actual work
    runtimes = []
    for op in operation:
        if op["type"] == "GET":
            start = time.time()
            cli.get(op["params"][0])
            end = time.time()
        elif op["type"] == "SET":
            start = time.time()
            cli.set(op["params"][0], op["params"][1])
            end = time.time()
        elif op["type"] == "POP":
            start = time.time()
            cli.delete(op["params"][0])
            end = time.time()
        runtimes.append((end-start) * 1e3)  # ms over s

    # Return stats
    return {
        "operations": len(operation),
        "time": sum(runtimes),
        "low": min(runtimes),
        "high": max(runtimes),
        "mean": mean(runtimes),
        "median": median(runtimes)
    }



def test_redis(nproc, nop):
    """
    Launch ``nproc`` number of processes (i.e. measure of concurrency).
    """
    op = list(operations(nop, seed_val=nproc))
    window = nop // nproc
    stats = []
    processes = []
    with ProcessPoolExecutor(nproc) as executor:
        for p in range(nproc):
            processes.append(executor.submit(redis_worker, op[window*p:window*(p+1)]))

    for p in processes:
        stats.append(p.result())

    return combine_stats(stats)



def main():
    n_operations = 1000
    global_stats = []

    # Launch redis-server and make sure to kill it before exiting
    # Server launch time is NOT calculated (for obvious reasons duh!)
    redis_server = subprocess.Popen(["redis-server", "--port", "54321"],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for concurrency in (1, 5, 10, 20):
        stats = test_lilcache(concurrency, n_operations)
        global_stats.append(
            ["lilcache", concurrency, n_operations, stats["mean"], stats["low"], stats["high"]]
        )
        stats = test_redis(concurrency, n_operations)
        global_stats.append(
            ["redis", concurrency, n_operations, stats["mean"], stats["low"], stats["high"]]
        )

    print(tabulate.tabulate(
        global_stats,
        headers=["Cache type", "Concurrency", "Number of operations (get/set/delete)",
                 "Mean response time (ms)", "Lowest time (ms)", "Highest time (ms)"],
        tablefmt="grid"
        ))

    redis_server.terminate()


if __name__ == "__main__":
    main()
