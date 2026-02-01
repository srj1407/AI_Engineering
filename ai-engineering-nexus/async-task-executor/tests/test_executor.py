import asyncio
import pytest
from async_task_executor.executor import AsyncTaskExecutor
from async_task_executor.models import Task

attempt_count = 0


async def success_task(i):
    await asyncio.sleep(0.5)
    return "Success"


async def failure_task(i):
    await asyncio.sleep(0.5)
    raise ValueError("Intentional failure")


async def long_task():
    await asyncio.sleep(1)
    return "Success"


async def very_long_task():
    await asyncio.sleep(5)
    return "Success"


async def flaky_task():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ValueError("Flaky failure")
    return "Success"


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
    time = end_time - start_time

    # Assert: Takes ~3 seconds (not 5 and not 1)
    assert 3 <= time < 4


@pytest.mark.asyncio
async def test_empty_task_list():
    executor = AsyncTaskExecutor(max_concurrent=2)
    report = await executor.run([])
    assert report.total_tasks == 0


@pytest.mark.asyncio
async def test_no_resource_leaks():
    """Verify all tasks are cleaned up"""

    executor = AsyncTaskExecutor(max_concurrent=3)
    tasks = [Task(func=success_task) for _ in range(3)]
    tasks = [Task(func=failure_task) for _ in range(3)]

    await executor.run(tasks)

    # Check no pending tasks remain
    pending = asyncio.all_tasks()
    assert len(pending) == 1  # Only main task should remain


@pytest.mark.asyncio
async def test_timeout_enforcement():
    """Test that tasks exceeding timeout are killed"""

    executor = AsyncTaskExecutor(max_concurrent=2)
    tasks = [Task(func=very_long_task, timeout=1.0)]
    executor_report = await executor.run(tasks)
    assert executor_report.results[0].error == "TimeoutError"


@pytest.mark.asyncio
async def test_retry_success():
    """Test that flaky tasks eventually succeed with retries"""

    executor = AsyncTaskExecutor(max_concurrent=2)
    tasks = [Task(func=flaky_task, retry=3)]
    executor_report = await executor.run(tasks)
    assert executor_report.results[0].success is True
    assert executor_report.results[0].attempt_count == 3


@pytest.mark.asyncio
async def test_exponential_backoff():
    """Test that backoff timing is correct"""

    executor = AsyncTaskExecutor(max_concurrent=2)
    tasks = [Task(func=failure_task, retry=3, backoff_factor=2)]
    executor_report = await executor.run(tasks)
    total_time = executor_report.results[0].execution_time
    assert 13 <= total_time <= 15


if __name__ == "__main__":
    asyncio.run(test_all_success())
    asyncio.run(test_partial_failure())
    asyncio.run(test_concurrency_limit())
    asyncio.run(test_empty_task_list())
    asyncio.run(test_no_resource_leaks())
    asyncio.run(test_timeout_enforcement())
    asyncio.run(test_retry_success())
    asyncio.run(test_exponential_backoff())
