import multiprocessing
import asyncio
import time

import aiohttp
import constants

NUM_WORKERS = 16


async def worker(start, end):
    session = aiohttp.ClientSession()
    tasks = [session.get(f'{constants.API_URL}/{x}') for x in range(start, end)]
    results = await asyncio.gather(*tasks)
    responses = await asyncio.gather(*[res.json() for res in results])
    await session.close()
    return sum([element['value'] for element in responses])


def main(start, end):
    return asyncio.run(worker(start, end))


if __name__ == '__main__':
    start = time.time()

    slice_size = constants.TRIALS // NUM_WORKERS
    with multiprocessing.Pool(NUM_WORKERS) as pool:
        result = pool.starmap(main, [
            (x*slice_size, (x+1)*slice_size)
            for x in range(NUM_WORKERS)
        ])

    computed_sum = sum(result)
    time_taken = time.time() - start

    print(f'computed value {computed_sum} for {constants.TRIALS} trials in '
          f'{round(time_taken, 2)}s - took {round(time_taken / constants.TRIALS, 6)}s per download, '
          f'using {NUM_WORKERS} processes.\n'
          f'Downloading 1_000_000_000 files would take approximately '
          f'{round(time_taken / constants.TRIALS * 1_000_000_000 / 60 / 60 / 24, 2)} days.')
    print(
        f'{NUM_WORKERS}-Procs {round(time_taken / constants.TRIALS, 6)} '
        f'{round(time_taken / constants.TRIALS * 1_000_000_000 / 60 / 60 / 24, 2)}'
    )
