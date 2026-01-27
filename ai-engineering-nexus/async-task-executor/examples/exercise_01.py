import asyncio
from time import time

async def task1():
    print("Task 1: Starting")
    await asyncio.sleep(1)
    print("Task 1: Completed")

async def task2():
    print("Task 2: Starting")
    await asyncio.sleep(1)
    print("Task 2: Completed")

async def task3():
    print("Task 3: Starting")
    await asyncio.sleep(1)
    print("Task 3: Completed")

async def task4():
    print("Task 4: Starting")
    await asyncio.sleep(1)
    print("Task 4: Completed")

async def task5():
    print("Task 5: Starting")
    await asyncio.sleep(1)
    print("Task 5: Completed")

async def main():
    print("Starting all tasks concurrently...")
    start_time=time()
    asyncio.gather(task1(), task2(), task3(), task4(), task5())
    end_time=time()
    print(f"All tasks completed in {end_time - start_time:.2f} seconds")

asyncio.run(main())