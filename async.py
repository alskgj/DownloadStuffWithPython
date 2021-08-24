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
    tasks = [session.get(f'{constants.API_URL}/{x}')
             for x in range(constants.TRIALS)]
    results = await asyncio.gather(*tasks)
    responses = await asyncio.gather(*[res.json() for res in results])
    await session.close()
    computed_sum = sum([element['value'] for element in responses])

    time_taken = round(time.time()-start)
    print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
          f'{time_taken}s')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
