"""
    async.py
    ========

    Uses the asyncio framework to get all 10 urls.
    Note: Just using a for loop and awaiting the individual
    session.get calls individually does work, but is not faster than
    the simple.py version, since that way, only one get request is known
    to the event loop at any time (so awaiting doesn't resume another one).
    This results in the somewhat unwieldy asyncio.gather(*list) syntax.
"""

import time
import aiohttp
import asyncio
import constants


async def main():
    start = time.time()
    session = aiohttp.ClientSession()

    # for a billion tasks, this consumes ~8.5GB memory
    tasks = [session.get(f'{constants.API_URL}/{x}') for x in range(constants.TRIALS)]
    results = await asyncio.gather(*tasks)
    responses = await asyncio.gather(*[res.json() for res in results])
    await session.close()
    computed_sum = sum([element['value'] for element in responses])

    time_taken = time.time() - start

    print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
          f'{round(time_taken, 2)}s - took {round(time_taken / constants.TRIALS, 5)}s per download')
    print(f'Async {round(time_taken / constants.TRIALS, 6)} '
          f'{round(time_taken / constants.TRIALS * 1_000_000_000 / 60 / 60 / 24, 2)}')


if __name__ == '__main__':
    asyncio.run(main())

