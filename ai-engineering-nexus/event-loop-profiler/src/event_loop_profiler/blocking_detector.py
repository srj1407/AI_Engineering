import asyncio
import time
from typing import Callable, List, Optional
from .models import BlockingDetection, BlockingReport, ExecutionTimeline

class BlockingDetector:
    """
    Detects blocking operations in async code.
    
    Monitors event loop responsiveness and identifies when
    tasks are blocking (not yielding control).
    
    Strategy: Periodically check if event loop is responsive.
    If check is delayed, something is blocking.
    """
    
    def __init__(self, threshold_ms: float = 50.0):
        """
        Args:
            threshold_ms: Duration in milliseconds that's considered blocking
                         (default: 50ms is a reasonable threshold)
        """
        self.threshold_ms = threshold_ms
        self.detections: List[BlockingDetection] = []
        self._monitoring = False
        self._current_task_name  = None

    
    async def run_with_detection(
        self,
        task: Callable,
        task_name: str = "unnamed"
    ) -> tuple[ExecutionTimeline, Optional[any]]:
        """
        Run a task and detect blocking operations.
        
        Args:
            task: Async function to monitor
            task_name: Name for reporting
            
        Returns:
            BlockingReport with any detected blocking
        """
        # Your implementation
        # Hints:
        # - Run task and monitor concurrently
        # - Monitor checks event loop responsiveness periodically
        # - If monitor check is delayed, blocking is happening
        
        self._current_task_name = task_name
        self.detections = []
        self.monitoring = True

        monitor_task = asyncio.create_task(self._monitor_event_loop())

        try:
            if asyncio.iscoroutinefunction(task):
                result = await task()
            else:
                result = await task
        finally:
            self._monitoring = False
            await monitor_task

        total_blocking_time = sum(d.blocking_duration for d in self.detections)

        if self.detections:
            worst = max(self.detections, key=lambda d: d.blocking_duration)
            worst_offender = f"{worst.task_name} ({worst.blocking_duration:.2f}s)"
        else:
            worst_offender = None

        return BlockingReport(
            detections=self.detections.copy(),
            total_blocking_time=total_blocking_time,
            worst_offender=worst_offender
        ), result
    
    async def _monitor_event_loop(self):
        """
        Continuously monitor event loop responsiveness.
        
        Checks if scheduled tasks run on time.
        If there's a delay, event loop was blocked.
        """
        # Your implementation
        # Hints:
        # - Use asyncio.sleep(0.01) for frequent checks
        # - Measure expected vs actual time
        # - If actual > expected + threshold, it's blocking

        check_interval = 0.01  # 10ms

        while self._monitoring:
            expected_wake_time = time.perf_counter() + check_interval

            await asyncio.sleep(check_interval)

            actual_wake_time = time.perf_counter()
            
            delay_seconds = actual_wake_time - expected_wake_time
            delay_ms = delay_seconds * 100

            if delay_ms > self.threshold_ms:
                # Determine severity based on duration
                if delay_ms > 200:  # More than 200ms is critical
                    severity = "Critical"
                else:
                    severity = "Warning"
                
                detection = BlockingDetection(
                    task_name=self._current_task_name,
                    blocking_duration=delay_seconds,  # Store in seconds
                    timestamp=actual_wake_time,
                    severity=severity
                )
                self.detections.append(detection)