import requests
import constants
import time
import threading
import queue
TRIALS = 10


def download_one(x: int, q: queue.Queue):
    response = requests.get(f'{constants.API_URL}/{x}').json()
    q.put(response['value'])


start = time.time()
result_queue = queue.Queue()
tasks = [threading.Thread(target=download_one, args=(x, result_queue))
         for x in range(TRIALS)]
for t in tasks:
    t.start()
computed_sum = 0
for i in range(TRIALS):
    computed_sum += result_queue.get()
time_taken = round(time.time()-start)

print(f'computed value {computed_sum} for {TRIALS} trials in {time_taken}s')
