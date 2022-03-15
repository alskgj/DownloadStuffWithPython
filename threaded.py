"""
    threaded.py
    ===========

    Starts a new thread for each of the 10 urls this program fetches.
    Each thread puts its result in a queue after receiving it. The main
    program fetches values from that queue until all 10 values have been
    obtained.
"""


import queue
import threading
import time
import requests
import constants


def download_one(x: int, q: queue.Queue):
    response = requests.get(f'{constants.API_URL}/{x}').json()
    q.put(response['value'])


start = time.time()
result_queue = queue.Queue()
tasks = (threading.Thread(target=download_one, args=(x, result_queue))
         for x in range(constants.TRIALS))

for t in tasks:
    t.start()

computed_sum = 0
for i in range(constants.TRIALS):
    computed_sum += result_queue.get()
time_taken = time.time()-start

print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
      f'{round(time_taken, 2)}s - took {round(time_taken/constants.TRIALS, 4)}s per download')