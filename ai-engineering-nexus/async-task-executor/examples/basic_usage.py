import asyncio
from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task


async def task1():
    """Simulates a fast operation"""

    await asyncio.sleep(0.1)
    return "Task 1 completed"


async def task2():
    """Simulates a slow operation"""

    await asyncio.sleep(2)
    return "Task 2 completed"


async def task3():

    await asyncio.sleep(0.5)
    return "Task 3 completed"


async def task4():

    await asyncio.sleep(1)
    return "Task 4 completed"


async def task5():
    """Simulates a task that fails"""

    r = 1 / 0  # This will raise a ZeroDivisionError
    return r


async def main():
    # Create executor
    executor = AsyncTaskExecutor(max_concurrent=3)

    # Create task list
    tasks = [
        Task(func=task1),
        Task(func=task2),
        Task(func=task3),
        Task(func=task4),
        Task(func=task5),
    ]

    # Run tasks
    executor_report = await executor.run(tasks)

    # Print report
    print(executor_report)


if __name__ == "__main__":
    asyncio.run(main())
