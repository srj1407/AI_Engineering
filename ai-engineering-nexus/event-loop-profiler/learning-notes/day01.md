# Day 1: Event Loop Internals
## What is the Event Loop?
The event loop is a single-threaded, infinite loop (while True) that acts as the central manager for asynchronous tasks. 🎡 It doesn't run tasks in parallel; instead, it coordinates when each task gets to use the CPU. It spends its time checking which tasks are ready to progress and "polling" the operating system for I/O events (like data arriving on a network socket).

## How Tasks Are Scheduled
Tasks are managed through internal queues. When a task is created (e.g., via asyncio.create_task()), it enters a Ready Queue. 📋 In every "tick" or iteration, the loop:

Polls I/O: Asks the OS if any network/disk operations are finished.

Checks Timers: Sees if any sleep durations have expired.

Executes: Picks tasks from the Ready Queue and runs them one by one until they hit an await.

## When Does a Task Yield Control?
A task yields control back to the loop when it explicitly says "I am waiting." This happens during:

await: The most common way to pause and wait for another coroutine or I/O.

asyncio.sleep(n): Even sleep(0) yields control to let other tasks in the queue run. 🤝

I/O Operations: Waiting for network responses, database queries, or file reading.

Task Completion: When the function finishes and returns a result.

## Mental Model Diagram
Imagine a Single Stove Burner (the CPU) and a Chef (the Event Loop). 👨‍🍳

The Chef has a Recipe Board (the Task Queue).

The Chef starts boiling water (I/O task) and sets a timer.

Instead of staring at the pot, the Chef looks at the board, sees "Chop Onions," and does that until the timer rings.

The Chef only ever has one hand on one task at a time. If the Chef spends 10 minutes carving an ice sculpture (Blocking/CPU-bound task), the onions burn and the water boils over because the Chef never "checked the board."

## Key Insight
The loop is a co-op, not a democracy. 🤝 Asyncio relies on "Cooperative Multitasking," meaning the loop cannot force a task to stop. If a task doesn't use await, it holds the entire program hostage. This is why time.sleep() is "poison" in async code, but asyncio.sleep() is a "gift" to other tasks.