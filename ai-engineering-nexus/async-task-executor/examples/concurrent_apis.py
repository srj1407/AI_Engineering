"""
Demonstrates concurrent API calls with rate limiting.

Scenario: Fetching data from 20 different endpoints,
but API allows max 5 concurrent requests.
"""

import asyncio
from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task


async def api_call():
    """Simulates an API call."""

    await asyncio.sleep(0.1)
    return "Task 1 completed"


async def main():
    # Create executor
    executor = AsyncTaskExecutor(max_concurrent=5)

    # Create task list
    tasks = [Task(func=api_call) for _ in range(20)]

    # Run tasks
    executor_report = await executor.run(tasks)

    # Print report
    print(executor_report)


if __name__ == "__main__":
    asyncio.run(main())

"""
Just some notes:
Here total duration was coming like this ->

Tasks 1-5:   ~0.108s   (first batch, starts immediately at 0s)
Tasks 6-10:  ~0.220s   (waits for batch 1 to finish + 0.1s sleep)
Tasks 11-15: ~0.330s   (waits for batch 2 to finish + 0.1s sleep)
Tasks 16-20: ~0.444s   (waits for batch 3 to finish + 0.1s sleep)

Your execution_time measures from when the task starts (after acquiring the semaphore) to when it finishes. Tasks that wait in the queue longer will have higher execution times because:

Task starts start_time = time.perf_counter()
Waits for semaphore slot
Runs the function
execution_time = end_time - start_time (includes wait time)
To measure only actual task time, move start_time inside the semaphore:

async with self._sem:
    start_time = time.perf_counter()  # Start timing HERE
    for i in range(retries):
        # ... task execution ...
        execution_time = time.perf_counter() - start_time

This way, execution_time will be ~0.1s for all tasks (just the sleep duration), not including semaphore wait time.

"""
