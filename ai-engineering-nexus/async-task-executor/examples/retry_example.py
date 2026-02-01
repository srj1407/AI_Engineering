import asyncio
import random
import logging
from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task

# Counter to track attempts
attempt_count1 = 0
attempt_count2 = 0

logging.basicConfig(level=logging.DEBUG)


async def flaky_api_1():
    """Fails first 2 times, succeeds on 3rd"""

    global attempt_count1
    attempt_count1 += 1
    print(f"  Attempt {attempt_count1} for flaky_api_1")

    if attempt_count1 < 3:
        raise ConnectionError(f"API unavailable (attempt {attempt_count1})")
    return "Success!"


async def flaky_api_2():
    """Fails first 2 times, succeeds on 3rd"""

    global attempt_count2
    attempt_count2 += 1
    print(f"  Attempt {attempt_count2} for flaky_api_2")

    if attempt_count2 < 3:
        raise ConnectionError(f"API unavailable (attempt {attempt_count2})")
    return "Success!"


async def very_slow_task():
    """Takes too long, will timeout"""
    await asyncio.sleep(10)
    return "Done"


async def main():
    # Show retry behavior
    executor = AsyncTaskExecutor(max_concurrent=2)
    tasks = [Task(func=flaky_api_1, retry=3)]

    # Show retry and failure after retries
    tasks += [Task(func=flaky_api_2, retry=2)]

    # Show timeout behavior
    tasks += [Task(func=very_slow_task, timeout=1.0)]

    executor_report = await executor.run(tasks)

    print(executor_report.summary())
    print("\nTask Reports:")
    for result in executor_report.results:
        print(
            f"  Success: {result.success}, Attempts: {result.attempt_count}, Result: {result.result}, Error: {result.error}, Execution Time: {result.execution_time:.2f}s"
        )


if __name__ == "__main__":
    asyncio.run(main())
