import asyncio
import time
from typing import Callable, List
from .models import TaskExecution, ExecutionTimeline, BlockingDetection, BlockingReport
from .blocking_detector import BlockingDetector

class EventLoopMonitor:
    """
    Monitors async task execution and builds execution timeline.
    
    Tracks when tasks start, end, and how long they take.
    Useful for understanding event loop behavior and finding bottlenecks.
    """
    
    def __init__(self):
        self.executions: List[TaskExecution] = []
        self._start_time: float = 0.0
    
    async def _wrap_task(self, task_func: Callable, name: str) -> TaskExecution:
        """Wrap a task to record its execution"""
        start_time = time.perf_counter()
        result = await task_func()
        end_time = time.perf_counter()
        duration = end_time - start_time

        taskExecution = TaskExecution(task_name=name, start_time=start_time, end_time=end_time, duration=duration)

        return taskExecution
    
    async def run_with_monitoring(
        self, 
        tasks: List[Callable], 
        task_names: List[str] = None
    ) -> ExecutionTimeline:
        """
        Run async tasks and monitor their execution.
        
        Args:
            tasks: List of async functions to execute
            task_names: Optional names for tasks (for reporting)
            
        Returns:
            ExecutionTimeline with execution details
        """
        # Your implementation here
        # Hints:
        # - Wrap each task with timing logic
        # - Use asyncio.create_task() or gather()
        # - Record start/end times for each
        # - Build ExecutionTimeline from results

        if task_names is None:
            task_names = [f'Task: {i}' for i in ramge(len(tasks))]
        
        self._start_time = time.perf_counter()

        wrapped_tasks = [self._wrap_task(tasks[i], task_names[i]) for i in range(len(task_names))]

        self.executions = await asyncio.gather(*wrapped_tasks)
        
        end_time = time.perf_counter()

        duration = end_time - self._start_time

        executionTimeline = ExecutionTimeline(executions = self.executions, total_duration = duration)

        return executionTimeline
    
async def run_with_full_analysis(
    self,
    tasks: List[Callable],
    task_names: List[str] = None,
    detect_blocking: bool = True
) -> tuple[ExecutionTimeline, BlockingReport]:
    """
    Run tasks with both timing and blocking detection.
    
    Returns:
        (timeline, blocking_report)
    """
    # Your implementation
    # Should run tasks with monitoring AND blocking detection

    if task_names is None:
            task_names = [f'Task: {i}' for i in ramge(len(tasks))]
        
    self._start_time = time.perf_counter()

    wrapped_tasks = [self._wrap_task(tasks[i], task_names[i]) for i in range(len(task_names))]

    if detect_blocking:
        detector = BlockingDetector()
        report, timeline = detector.run_with_detection(asyncio.gather(*wrapped_tasks))

    self.executions = await asyncio.gather(*wrapped_tasks)
    
    end_time = time.perf_counter()

    duration = end_time - self._start_time

    executionTimeline = ExecutionTimeline(executions = self.executions, total_duration = duration)

    return executionTimeline