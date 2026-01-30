import asyncio
from async_task_executor.models import Task, TaskResult, ExecutionReport
from typing import List

class AsyncTaskExecutor:
    def __init__(self, max_concurrent):
        """Initialize the AsyncTaskExecutor with configuration parameters."""

        self.max_concurrent = max_concurrent
        self._sem = asyncio.Semaphore(max_concurrent)

    async def run(self, tasks: List[Task]) -> ExecutionReport:
        """The main method to run a list of tasks asynchronously."""

        results = await asyncio.gather(*[self._execute_task(task) for task in tasks], return_exceptions=True)
        return ExecutionReport(
            total_tasks=len(tasks),
            successful_count=sum(1 for r in results if r.success),
            failed_count=sum(1 for r in results if not r.success),
            results=results
        )

    async def _execute_task(self, task: Task) -> TaskResult:
        """Method to execute a single task asynchronously."""

        async with self._sem:
            try:
                start_time = asyncio.get_event_loop().time()
                res = await task.func(*task.args, **(task.kwargs or {}))
                end_time = asyncio.get_event_loop().time()
                return TaskResult(success=True, result=res, execution_time=end_time - start_time)
            except Exception as e:
                return TaskResult(success=False, error=str(e))
            
