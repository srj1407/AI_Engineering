from dataclasses import dataclass
from typing import Any, List
import time

@dataclass
class TaskExecution:
    """Record of a single task execution"""
    task_name: str
    start_time: float  # timestamp
    end_time: float    # timestamp
    duration: float    # seconds
    

@dataclass
class ExecutionTimeline:
    """Timeline of all task executions"""
    executions: List[TaskExecution]
    total_duration: float
    
    def print_execution(self) -> None:
        """Printing execution timeline"""

        res = []
        for exec in self.executions:
            res.append(f"Task: {exec.task_name}, Start: {time.ctime(exec.start_time)}, End: {time.ctime(exec.end_time)}, Duration: {exec.duration:.2f} seconds")
        return res

    def summary(self) -> str:
        """Return human-readable timeline"""
        return f"""Execution Timeline Summary:
              Total Duration: {self.total_duration:.2f} seconds
              Task Timeline: {self.print_execution()}
              """
    
@dataclass
class BlockingDetection:
    """Record of detected blocking operation"""
    task_name: str
    blocking_duration: float  # How long it blocked
    timestamp: float  # When it happened
    severity: str  # "Warning" or "Critical"
    
@dataclass
class BlockingReport:
    """Report of all blocking operations detected"""
    detections: List[BlockingDetection]
    total_blocking_time: float
    worst_offender: str  # Task with longest block
    
    def blocked_operations(self):
        """Return blocked operations"""

        res = []
        for op in self.detections:
            res.append(f"Task: {op.task_name}, Duration: {op.blocking_duration} seconds, End: {time.ctime(op.timestamp)}, Severity: {op.severity}")
        return res


    def summary(self) -> str:
        """Human-readable blocking report"""
        return f"""Blocking Summary:
              Total Blocking time: {self.total_blocking_time:.2f} seconds
              Worst offender: {self.worst_offender}
              Blocked operations: {self.blocked_operations()}
              """   