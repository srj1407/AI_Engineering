import asyncio
import pytest
from src.async_task_executor.executor import AsyncTaskExecutor
from src.async_task_executor.models import Task

async def success_task(i):
      await asyncio.sleep(i)
      return "success"
  
async def failure_task(i):
    await asyncio.sleep(i)
    raise ValueError("intentional failure")

async def long_task():
    await asyncio.sleep(1)
    return "success"

@pytest.mark.asyncio
async def test_all_success():
    """Test execution when all tasks succeed"""

    # Create executor
    executor = AsyncTaskExecutor(max_concurrent=3)

    # Create 5 simple tasks
    tasks = [Task(func=success_task, args=(i,)) for i in range(5)]

    # Run them
    executor_report = await executor.run(tasks)

    # Assert: report.successful == 5, report.failed == 0
    assert executor_report.successful_count == 5
    assert executor_report.failed_count == 0

@pytest.mark.asyncio
async def test_partial_failure():
    """Test execution when some tasks fail"""

    # Create executor
    executor = AsyncTaskExecutor(max_concurrent=3)

    # Create 3 success tasks + 2 failure tasks
    tasks = [Task(func=success_task, args=(i,)) for i in range(3)]
    tasks += [Task(func=failure_task, args=(i,)) for i in range(2)]

    # Run them
    executor_report = await executor.run(tasks)

    # Assert: report.successful == 3, report.failed == 2
    assert executor_report.successful_count == 3
    assert executor_report.failed_count == 2

@pytest.mark.asyncio
async def test_concurrency_limit():
    """Test that max_concurrent is respected"""

    # Create executor with max_concurrent=2
    executor = AsyncTaskExecutor(max_concurrent=2)

    # Create 5 tasks that each take 1 second
    tasks = [Task(func=long_task) for i in range(5)]
    
    # Run them
    start_time = asyncio.get_event_loop().time()
    executor_report = await executor.run(tasks)
    end_time = asyncio.get_event_loop().time()

    # Measure total time
    time= end_time - start_time

    # Assert: Takes ~3 seconds (not 5 and not 1)
    assert 3 <= time < 4

if __name__ == "__main__":
    asyncio.run(test_all_success())
    asyncio.run(test_partial_failure())
    asyncio.run(test_concurrency_limit())