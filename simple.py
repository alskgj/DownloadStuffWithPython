"""
    simple.py
    =========

    Fetches 10 urls one by one.
"""

import requests
import constants
import time

session = requests.session()


def download_one(x):
    value = session.get(f'{constants.API_URL}/{x}').json()
    return value


start = time.time()
computed_sum = 0
for i in range(constants.TRIALS):
    computed_sum += download_one(i)['value']
time_taken = time.time()-start

print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
      f'{round(time_taken, 2)}s - took {round(time_taken/constants.TRIALS, 6)}s per download, '
      f'Downloading 1_000_000_000 files would take approximately '
      f'{round(time_taken/constants.TRIALS*1_000_000_000/60/60/24, 2)} days.')
print(f'Simple {round(time_taken/constants.TRIALS, 6)} {round(time_taken/constants.TRIALS*1_000_000_000/60/60/24, 2)}')
