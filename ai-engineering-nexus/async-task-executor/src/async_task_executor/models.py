from dataclasses import dataclass
from typing import Callable, Any, Dict, List, Optional


@dataclass
class Task:
    """Represents a single task that needs to be executed."""

    func: Callable
    args: tuple = ()
    kwargs: Dict[str, Any] = None
    timeout: float = 3.0
    retry: int = 3
    backoff_factor: float = 0.5


@dataclass
class TaskResult:
    """Represents the result of execution"""

    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    attempt_count: int = 1


@dataclass
class ExecutionReport:
    """Represents summary of all executions"""

    total_tasks: int
    successful_count: int
    failed_count: int
    results: List[TaskResult]

    def summary(self) -> str:
        """Return human-readable summary of execution"""
        # Your implementation
        return (
            f"Execution Report:\n"
            f"Total Tasks: {self.total_tasks}\n"
            f"Successful: {self.successful_count}\n"
            f"Failed: {self.failed_count}\n"
            f"Success Rate: {self.successful_count / self.total_tasks * 100:.2f}%"
        )
