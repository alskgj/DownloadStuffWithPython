Download Stuff With Python
==========================

This is a demonstration on how to download stuff with Python3.

## Installation
Install the dependencies with
```
python3 -m pip install -r requirements.txt
```

Then run the webserver script, it exposes a rest api simulating a real server. To test if you launched the server correctly you can visit the docs at http://127.0.0.1:8000/docs.

## Examples

There are currently 3 examples
```properties
simple.py Fetch urls one after another
threaded.py Fetch urls using Threads
async.py Fetch urls using asyncio
optimized.py async.py with some optimizations
```

They all fetch the resources at (with n configurable at constants.TRIALS)
```
http://127.0.0.1:8000/0
http://127.0.0.1:8000/1
...
http://127.0.0.1:8000/n-1
```

the webserver waits one second until answering a request, to simulate a slow website.

## Expected behaviour

### With constants.TRIALS = 100
```properties
simple.py:    computed value 4950 for 100 trials in 100s
threaded.py:  computed value 4950 for 100 trials in 1s
async.py:     computed value 4950 for 100 trials in 1s
optimized.py: computed value 4950 for 100 trials in 1s
```

### With constants.TRIALS = 10000
Values this high bottleneck on stuff not directly related to the example files:
- simple.py runs fine (but very slowly)
- threaded.py will crash something, either itself, your webserver, or your os
- async.py  will probably bottleneck the webserver
- optimized.py uses multiple sessions to workaround the built-in throtting mechanisms
  of the webserver.

On my machine this was:
```properties
simple.py:    computed value 49995000 for 10000 trials in 10000s
threaded.py:  <crashed>
async.py:     computed value 49995000 for 10000 trials in 101s
optimized.py: computed value 49995000 for 10000 trials in 12s
```

Note: `optimized.py` already downloads 1'000 pages per second in this example, 
using only a single core. If you need much more than that many things start to become an 
issue, such as OS limits, the webserver on the other side, or simply bandwidth from
the payloads or even just the request overhead.

However, if those are not a concern, the way to go is combining the threaded and 
async approaches, essentially running a version of `optimized.py` on each available
core.
