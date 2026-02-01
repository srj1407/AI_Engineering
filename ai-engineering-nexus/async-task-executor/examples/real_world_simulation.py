"""
Simulates a realistic production scenario:
- Multiple LLM API calls (some fast, some slow)
- Network flakiness (random failures)
- Rate limiting (max 10 concurrent)
- Mixed timeouts (1s, 5s, 10s)

Shows how AsyncTaskExecutor handles production complexity.
"""

from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task

import asyncio


async def task1():
    await asyncio.sleep(1)
    return "Task 1 completed"


async def task2():
    await asyncio.sleep(3)
    return "Task 2 completed"


async def task3():
    await asyncio.sleep(7)
    return "Task 3 completed"


async def flaky_task():
    import random

    await asyncio.sleep(2)
    if random.random() < 0.3:
        raise ValueError("Simulated network error")
    return "Flaky task succeeded"


async def task():
    # Create executor with max 10 concurrent tasks
    executor = AsyncTaskExecutor(max_concurrent=10)

    # Create a mix of tasks with different timeouts
    tasks = [
        Task(func=task1, timeout=2),
        Task(func=task2, timeout=4),
        Task(func=task3, timeout=6),
    ] + [Task(func=flaky_task, timeout=5, retry=2) for _ in range(20)]

    # Run tasks
    executor_report = await executor.run(tasks)

    # Print summary
    for task_result in executor_report.results:
        print(
            f"Success: {task_result.success}, Result: {task_result.result}, Error: {task_result.error}, Time: {task_result.execution_time:.2f}s, Attempts: {task_result.attempt_count}"
        )

    print(executor_report.summary())


if __name__ == "__main__":
    asyncio.run(task())
