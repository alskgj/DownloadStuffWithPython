"""
    simple.py
    =========

    Fetches 10 urls one by one.
"""

import requests
import constants
import time


def download_one(x):
    value = requests.get(f'{constants.API_URL}/{x}').json()
    return value


start = time.time()
computed_sum = 0
for i in range(constants.TRIALS):
    computed_sum += download_one(i)['value']
time_taken = round(time.time()-start)

print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
      f'{time_taken}s')
