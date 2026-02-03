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