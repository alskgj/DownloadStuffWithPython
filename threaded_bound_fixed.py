"""
    threaded.py
    ===========

    Starts a new thread for each of the 10 urls this program fetches.
    Each thread puts its result in a queue after receiving it. The main
    program fetches values from that queue until all values have been
    obtained.
"""

import queue
import threading
import time
import requests
import constants

NUM_WORKERS = 10000


def download_one(x: int, q: queue.Queue, session: requests.Session):
    response = session.get(f'{constants.API_URL}/{x}')
    q.put(response.json()['value'])


def worker(first: int, last: int, q: queue.Queue):
    session = requests.Session()
    partial_sum = 0
    for i in range(first, last):
        response = session.get(f'{constants.API_URL}/{i}')
        partial_sum += response.json()['value']
    q.put(partial_sum)



start = time.time()
result_queue = queue.Queue()

slice_size = constants.TRIALS // NUM_WORKERS
workers = [
    threading.Thread(target=worker, args=(x*slice_size, (x+1)*slice_size, result_queue))
    for x in range(NUM_WORKERS)
]

for t in workers:
    t.start()

computed_sum = 0
for i in range(NUM_WORKERS):
    computed_sum += result_queue.get()
time_taken = time.time()-start

print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
      f'{round(time_taken, 2)}s - took {round(time_taken/constants.TRIALS, 6)}s per download, '
      f'using {NUM_WORKERS} threads.\n'
      f'Downloading 1_000_000_000 files would take approximately '
      f'{round(time_taken/constants.TRIALS*1_000_000_000/60/60/24, 2)} days.')
print(f'{NUM_WORKERS}-Threads {round(time_taken/constants.TRIALS, 6)} {round(time_taken/constants.TRIALS*1_000_000_000/60/60/24, 2)}')
