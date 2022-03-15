"""
    optimized.py
    ============

    - uses multiple sessions
    - setting a high number of sessions will eventually crash the webserver
"""

import time
import aiohttp
import asyncio
import constants

SESSION_N = 10


async def main():
    start = time.time()
    sessions = [aiohttp.ClientSession() for i in range(SESSION_N)]

    tasks = []
    slice_size = constants.TRIALS//SESSION_N
    for i, session in enumerate(sessions):
        tasks += [session.get(f'{constants.API_URL}/{x}')
                  for x in range(i*slice_size, (i+1)*slice_size)]

    results = await asyncio.gather(*tasks)
    responses = await asyncio.gather(*[res.json() for res in results])
    computed_sum = sum([element['value'] for element in responses])

    time_taken = time.time() - start

    print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
          f'{round(time_taken, 2)}s - took {round(time_taken / constants.TRIALS, 5)}s per download')
    print(f'Async+ {round(time_taken / constants.TRIALS, 6)} {round(time_taken / constants.TRIALS * 1_000_000_000 / 60 / 60 / 24, 2)}')
    for session in sessions:
        await session.close()

if __name__ == '__main__':
    asyncio.run(main())