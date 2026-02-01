"""
Demonstrates graceful failure handling.

Scenario: Processing 100 items where some will fail.
We want to continue processing and collect both
successes and failures for later analysis.
"""

import asyncio
from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task


async def success_task():
    await asyncio.sleep(0.5)
    return "Success"


async def failure_task():
    await asyncio.sleep(0.5)
    raise ValueError("Intentional failure")


async def task():
    """Test execution when some tasks fail"""

    # Create executor
    executor = AsyncTaskExecutor(max_concurrent=3)

    # Create 3 success tasks + 2 failure tasks
    tasks = [Task(func=success_task) for i in range(30)]
    tasks += [Task(func=failure_task) for i in range(70)]

    # Run them
    executor_report = await executor.run(tasks)

    # Print summary
    print(executor_report.summary())


if __name__ == "__main__":
    asyncio.run(task())
