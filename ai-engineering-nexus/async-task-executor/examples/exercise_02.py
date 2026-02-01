import asyncio
import time

sem = asyncio.Semaphore(3)


async def task(i):
    async with sem:
        print(f"Task {i} started")
        await asyncio.sleep(2)
        print(f"Task {i} finished")


async def main():
    start_time = time.time()
    await asyncio.gather(*(task(i) for i in range(10)))
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")


asyncio.run(main())
