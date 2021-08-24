import time

import aiohttp
import asyncio

import constants

TRIALS = 10


async def main():
    start = time.time()
    session = aiohttp.ClientSession()
    tasks = [session.get(f'{constants.API_URL}/{x}') for x in range(TRIALS)]
    results = await asyncio.gather(*tasks)
    responses = await asyncio.gather(*[res.json() for res in results])
    await session.close()
    computed_sum = sum([element['value'] for element in responses])

    time_taken = round(time.time()-start)
    print(f'computed value {computed_sum} for {TRIALS} trials in {time_taken}s')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
