"""
task 1:
download 'http://127.0.0.1:8000/123' five times and print the results

task 2:
download 'http://127.0.0.1:8000/1', 'http://127.0.0.1:8000/2', ..., 'http://127.0.0.1:8000/20' and print the results

task 3:
do task 2 in under 1.1 seconds

bonus task 4:
download 10'000 urls in under 20 seconds without crashing my computer

"""
import asyncio
import time

import requests
import aiohttp

import threading
from queue import Queue

url = 'http://127.0.0.1:8000/123'
base_url = 'http://127.0.0.1:8000/'


def task_1(request_url):
    start = time.perf_counter()
    resps = []
    for i in range(5):
        resp = requests.get(request_url).json()
        resps.append(resp["value"])

    end = time.perf_counter()
    time_taken = end - start

    return f"Done in {time_taken}s.\nValues: {resps}"

# print(task_1(url))


def task_2(base_url: str, amount: int):
    start = time.perf_counter()
    resps = []
    for i in range(amount):
        resp = requests.get(f"{base_url}{i}").json()
        resps.append(resp["value"])

    end = time.perf_counter()
    time_taken = end - start

    return f"Done in {time_taken}s. \nValues: {resps}"

# print(task_2(base_url, 20))


def task_3_worker(base_url: str, value: int, q):
    resp = requests.get(f"{base_url}{value}").json()

    q.put(resp["value"])


def task_3(base_url: str, amount: int):
    start = time.perf_counter()
    queue = Queue()
    values = []

    for i in range(amount):
        threading.Thread(target=task_3_worker, args=(base_url, i, queue,)).start()

    for i in range(amount):
        values.append(queue.get())
        values = sorted(values)

    end = time.perf_counter()
    time_taken = end - start

    return f"Done in {time_taken}s. \nValues: {values}"

# print(task_3(base_url, 100000))


async def task_3_worker_asyncio(base_url: str, value: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}{value}") as response:
            resp = await response.json()
    return resp["value"]


async def task_3_asyncio(base_url: str, amount: int):
    values = []

    for i in range(amount):
        value = await task_3_worker_asyncio(base_url, i)
        values.append(value)

    print('got values', values)

    return values


def run_task_3_asyncio(base_url: str, amount: int):
    asyncio.run(task_3_asyncio(base_url, amount))

start = time.perf_counter()

print(run_task_3_asyncio(base_url, 20))

end = time.perf_counter()
time_taken = end - start
print(time_taken)

# done in x seconds
# got values: [123, 123, 123, 123, 123]
