## Day 2: Blocking Operations

What Makes Code Blocking?
Blocking operations are functions that "hog" the CPU or the thread's execution, preventing the event loop from moving to the next task.

• time.sleep(): Blocks the entire thread; the loop cannot "tick."

• requests.get() / urllib: Synchronous HTTP calls that wait for a network response without yielding.

• Heavy CPU Bound Tasks: Complex math, image processing, or large JSON parsing.

• Standard File I/O: `open().read()` is synchronous and can block if the disk is slow.

• Blocking Socket Calls: Any network call not wrapped in an `awaitable`.

How Blocking Code Affects Event Loop
When a synchronous function runs inside an `async` function, it occupies the single thread of the event loop. Because there is no `await` keyword to create a "yield point," the loop cannot pause the task. Every other task in the "Ready Queue" remains frozen until the blocking call returns.

Detection Strategy
• asyncio Debug Mode: Use `loop.set_debug(True)`. This monitors how long callbacks take.

• Slow Callback Threshold: Set `loop.slow_callback_duration = 0.1` to log warnings for any task taking longer than 100ms.

• Execution Monitors: Using `time.perf_counter()` in a background task to detect "heartbeat" gaps.

Key Insight
Async is not parallel. Calling a synchronous function inside an `async def` doesn't make it faster or "backgrounded"; it actually makes it more dangerous because it breaks the "cooperative" contract that the entire program relies on.