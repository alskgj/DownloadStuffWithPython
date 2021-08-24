"""
    threaded.py
    ===========

    Starts a new thread for each of the 10 urls this program fetches.
    Each thread puts its result in a queue after receiving it. The main
    program fetches values from that queue until all 10 values have been
    obtained.
"""


import requests
import constants
import time
import threading
import queue


def download_one(x: int, q: queue.Queue):
    response = requests.get(f'{constants.API_URL}/{x}').json()
    q.put(response['value'])


start = time.time()
result_queue = queue.Queue()
tasks = [threading.Thread(target=download_one, args=(x, result_queue))
         for x in range(constants.TRIALS)]
for t in tasks:
    t.start()
computed_sum = 0
for i in range(constants.TRIALS):
    computed_sum += result_queue.get()
time_taken = round(time.time()-start)

print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
      f'{time_taken}s')
