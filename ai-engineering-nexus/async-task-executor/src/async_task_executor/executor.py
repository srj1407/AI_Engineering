import asyncio
import logging
import time
from async_task_executor.models import Task, TaskResult, ExecutionReport
from typing import List
import random


class AsyncTaskExecutor:
    """
    Concurrent async task executor with retry and timeout support.

    Manages execution of multiple async tasks with configurable
    concurrency limits, per-task timeouts, and intelligent retry
    with exponential backoff.

    Attributes:
        max_concurrent (int): Maximum number of tasks running simultaneously
        default_timeout (float): Default timeout in seconds for tasks

    Example:
        >>> executor = AsyncTaskExecutor(max_concurrent=5)
        >>> tasks = [Task(fetch_data, args=(url,)) for url in urls]
        >>> report = await executor.run(tasks)
        >>> print(f"Success: {report.successful}, Failed: {report.failed}")
    """

    def __init__(self, max_concurrent):
        """Initialize the AsyncTaskExecutor with configuration parameters."""

        self.max_concurrent = max_concurrent
        self._sem = asyncio.Semaphore(max_concurrent)

    async def run(self, tasks: List[Task]) -> ExecutionReport:
        """
        Execute all tasks concurrently and return execution report.

        Tasks are executed with concurrency limiting, timeout enforcement,
        and retry logic. Failures are isolated - one task's failure does
        not affect others.

        Args:
            tasks: List of Task objects to execute

        Returns:
            ExecutionReport containing results and summary

        Example:
            >>> tasks = [Task(my_func, args=(1,)), Task(my_func, args=(2,))]
            >>> report = await executor.run(tasks)
        """

        results = await asyncio.gather(
            *[self._execute_task(task) for task in tasks], return_exceptions=True
        )
        return ExecutionReport(
            total_tasks=len(tasks),
            successful_count=sum(1 for r in results if r.success),
            failed_count=sum(1 for r in results if not r.success),
            results=results,
        )

    async def _execute_task(self, task: Task) -> TaskResult:
        """Method to execute a single task asynchronously.

        Args:
            task: Task object to execute

        Returns:
            TaskResult containing the outcome of the task

        Example:
            >>> result = await executor._execute_task(task)

        """

        task_name = task.func.__name__
        logger = logging.getLogger(__name__)
        logger.debug(f"Executing task: {task_name}")
        start_time = time.perf_counter()
        errorMsg = None
        retries = task.retry
        timeout = task.timeout
        backoff = task.backoff_factor
        attempt = 0
        async with self._sem:
            for i in range(retries):
                attempt += 1
                try:
                    res = await asyncio.wait_for(
                        task.func(*task.args, **(task.kwargs or {})), timeout=timeout
                    )
                    return TaskResult(
                        success=True,
                        result=res,
                        execution_time=time.perf_counter() - start_time,
                        attempt_count=attempt,
                    )
                except asyncio.TimeoutError as e:
                    errorMsg = "TimeoutError"
                    return TaskResult(
                        success=False,
                        error=errorMsg,
                        execution_time=time.perf_counter() - start_time,
                        attempt_count=attempt,
                    )
                except Exception as e:
                    logger.error(f"Error in task {task_name}: {e}")
                    errorMsg = str(e)
                    delay = backoff * (2 ** (i))
                    # jittered_delay = random.uniform(0, delay)
                    await asyncio.sleep(delay)
                    logger.info(
                        f"Retrying task {task_name} (attempt {attempt + 1}/{retries})"
                    )
            return TaskResult(
                success=False,
                error=errorMsg,
                execution_time=time.perf_counter() - start_time,
                attempt_count=attempt,
            )
