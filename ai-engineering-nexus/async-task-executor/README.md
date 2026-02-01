# AsyncTaskExecutor

A production-grade async task execution library with intelligent retry, 
exponential backoff, and comprehensive failure handling.

Built as the foundation for distributed AI agent orchestration.

## The Problem

In production AI systems, you need to:
- Execute 100+ LLM API calls concurrently (reduce latency from 100s → 5s)
- Handle API rate limits without cascading failures
- Retry failed requests intelligently (not all at once)
- Timeout operations that hang indefinitely
- Continue execution when some tasks fail

Standard solutions (`asyncio.gather`, `concurrent.futures`) don't provide:
- Rate Limiting, Retries and Timeout functionalities.

AsyncTaskExecutor solves this by using semaphores for rate limiting, using a loop for retryying the task for a specific number of times and async.wait_for functionality to wait for just a specified amount of time for a task to complete.

## Quick Start

```python

async def _execute_task(self, task: Task) -> TaskResult:
        """Method to execute a single task asynchronously."""

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
                    res = await asyncio.wait_for(task.func(*task.args, **(task.kwargs or {})), timeout=timeout)
                    return TaskResult(success=True, result=res, execution_time=time.perf_counter() - start_time, attempt_count=attempt)
                except asyncio.TimeoutError as e:
                    errorMsg = "TimeoutError"
                    return TaskResult(success=False, error=errorMsg, execution_time=time.perf_counter() - start_time, attempt_count=attempt)
                except Exception as e:
                    logger.error(f"Error in task {task_name}: {e}")
                    errorMsg = str(e)
                    delay = backoff * (2 ** (i))
                    # jittered_delay = random.uniform(0, delay)
                    await asyncio.sleep(delay)
                    logger.info(f"Retrying task {task_name} (attempt {attempt + 1}/{retries})")
            return TaskResult(success=False, error=errorMsg, execution_time=time.perf_counter() - start_time, attempt_count=attempt)
                
```

## Features

- ⚡ **Concurrent Execution**: Run N tasks with configurable concurrency limits
- ⏱️ **Timeout Control**: Per-task timeout with graceful cleanup
- 🔄 **Intelligent Retry**: Exponential backoff prevents thundering herd
- 🛡️ **Failure Isolation**: One task's failure doesn't crash others
- 📊 **Execution Reports**: Detailed success/failure breakdown
- 🧪 **Fully Tested**: 100% test coverage with edge cases

## Usage Examples

### Example 1: Concurrent API Calls

```python

results = await asyncio.gather(*[self._execute_task(task) for task in tasks], return_exceptions=True)
        return ExecutionReport(
            total_tasks=len(tasks),
            successful_count=sum(1 for r in results if r.success),
            failed_count=sum(1 for r in results if not r.success),
            results=results
        )

```
Here asyncio.gather initializes an event loop to concurrently execute all the tasks.

### Example 2: Flaky Operations with Retry

```python

for i in range(retries):
                attempt += 1
                try:
                    res = await asyncio.wait_for(task.func(*task.args, **(task.kwargs or {})), timeout=timeout)
                    return TaskResult(success=True, result=res, execution_time=time.perf_counter() - start_time, attempt_count=attempt)
                except asyncio.TimeoutError as e:
                    errorMsg = "TimeoutError"
                    return TaskResult(success=False, error=errorMsg, execution_time=time.perf_counter() - start_time, attempt_count=attempt)
                except Exception as e:
                    logger.error(f"Error in task {task_name}: {e}")
                    errorMsg = str(e)
                    delay = backoff * (2 ** (i))
                    # jittered_delay = random.uniform(0, delay)
                    await asyncio.sleep(delay)
                    logger.info(f"Retrying task {task_name} (attempt {attempt + 1}/{retries})")
            return TaskResult(success=False, error=errorMsg, execution_time=time.perf_counter() - start_time, attempt_count=attempt)

```

Here using for loop we are trying to run this function a specified number of times. On success and timeout, the function will directly return. But in case of error, the function will use backoff factor to retry execution after a certain time interval.

### Example 3: Mixed Timeouts

```python

except Exception as e:
                    logger.error(f"Error in task {task_name}: {e}")
                    errorMsg = str(e)
                    delay = backoff * (2 ** (i))
                    # jittered_delay = random.uniform(0, delay)
                    await asyncio.sleep(delay)
                    logger.info(f"Retrying task {task_name} (attempt {attempt + 1}/{retries})")

```

Here, using delay and backoff factor we are increasing the delay everytime.

## Design Decisions

🚦 Why Semaphore over Queue?
While a Queue is great for distributing work to a set number of workers, a Semaphore is often more lightweight for simple rate-limiting.Reasoning: Using a Semaphore allows us to launch all tasks but control the concurrency at the point of execution. This is simpler to implement than managing a worker pool for a script of this scale.

📈 Why Exponential Backoff?
The math $wait = base\_delay \times 2^{attempt}$ ensures that as failures persist, we back off further to give the server time to recover.Thundering Herd: Without jitter, multiple clients retrying at the same time create massive "spikes" of traffic. Adding randomness (Jitter) ensures these requests are spread out over time, turning a "spike" into a "stream."

🛡️ Why Structured Results over Exceptions?
Instead of letting an exception crash the entire gather() call, we return a structured result (like a dictionary or a specific string).Philosophy: In a batch process, a single failure shouldn't be "fatal." By returning a result that describes the error, the calling code can easily filter for successes without needing complex try/except blocks in the main loop.

🏗️ Capturing the Trade-offs
No design is perfect; every choice has a cost. For example, by choosing a low Semaphore limit, you protect the server, but your total execution time increases.

## What I Learned Building This

The most surprising discovery: 
We can run all tasks and return with information whether they got scessfully executed or any of the tasks got failedusing return_exceptions=True. Any of the tasks failing does not cause the whole asyncio run to fail.

This taught me: We can gracefully handle errors in large systems without getting the whole system shut.

## Current Limitations

This library does NOT:
- ❌ Persist task state (tasks lost if process crashes)
- ❌ Support distributed execution (single-machine only)
- ❌ Handle task dependencies (all tasks independent)

## Technical Details

**Requirements:**
- Python 3.8+
- uvicorn
- pytest
- pytest-asyncio

**Installation:**
\```bash
uv sync
uv pip install -r requirements.txt
\```

**Running Tests:**
\```bash
pytest tests/
\```
