# Day 03: Asyncio gather() vs create_task () and Exception Handling in Async

🐍 Asyncio Mastery: Concurrency & Control
1. Task Creation vs. Result Gathering
There are two primary ways to manage concurrent operations in Python. Selecting the right one depends on whether you need individual control or a collective result.

asyncio.create_task(): Best for "fire and forget" or background tasks. It returns a Task object immediately, allowing you to interact with it (cancel, check status) while other code runs.

asyncio.gather(): Best for grouping multiple coroutines and waiting for all results. It returns a single list containing all returned values in the order they were provided.

| Feature | create_task | gather |
|---------|------------|--------|
| Input | A single coroutine | Multiple awaitables (unpacked) |
| Output | A Task handle | A list of results |
| Use Case | Background workers | Batch API requests |

```python

# Gathering multiple results into a list
results = await asyncio.gather(task1(), task2(), task3())

```

2. Robust Exception Handling 🛠️
In asynchronous programming, a single failure can crash your entire event loop if not handled correctly.

The return_exceptions Parameter
By default, gather() raises the first exception it encounters. Setting return_exceptions=True tells gather to treat exceptions as valid results and place them in the output list.

Internal try/except: Handles errors inside the coroutine to return a "fallback" (like None).

External gather Handling: Use isinstance(res, Exception) to check the results list for errors that slipped through.

3. Timeouts and Safety ⏱️
Tasks that hang indefinitely can block your application's progress. We use asyncio.wait_for() to enforce strict deadlines.

Granular Control: Wrapping individual coroutines in a timeout allows one slow task to fail while others succeed.

The TimeoutError: Always wrap wait_for in a try/except block to handle the specific asyncio.TimeoutError.

Example:

```python

try:
    result = await asyncio.wait_for(my_coroutine(), timeout=2.0)
except asyncio.TimeoutError:
    result = "Timed out"

```

4. Throttling Concurrency with Semaphores 🚦
A Semaphore (asyncio.Semaphore) limits the number of concurrent tasks. This prevents overwhelming a database or being rate-limited by an API.

Mechanism: Tasks must "acquire" a permit to run and "release" it when finished.

Implementation: Use the async with sem: context manager inside your coroutine.

Consolidated Code Example:

```python

import asyncio

sem = asyncio.Semaphore(3) # Limit to 3 concurrent downloads

async def safe_download(img_id):
    async with sem: # Throttle here
        try:
            # Add a timeout for the individual operation
            return await asyncio.wait_for(simulate_api(img_id), timeout=5.0)
        except (asyncio.TimeoutError, Exception):
            return None # Return fallback on failure

async def simulate_api(img_id):
    await asyncio.sleep(1)
    return f"Data for {img_id}"

async def main():
    ids = range(1, 11)
    tasks = [safe_download(i) for i in ids]
    # Gather all results, treating exceptions as items in the list
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())

```

**Some other important points**

1. uv package root directory contains pyproject.toml file. There u need to specify your root directory name. After that all imports will look into src folder with a folder of that root name. And then from there relative path starts.

2. To execute tasks using async with sem and exception handling you need to give the try/except block inside async with sem.

3. A failed task does not return anything and the lines after failing await task.execute line will not run. You can just use exception handling and return exception message.

4. assert can be used for testing and returning test results.