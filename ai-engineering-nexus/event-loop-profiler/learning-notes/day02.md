## Day 2: Blocking Operations

1. What Makes Code Blocking?
Blocking operations are functions that "hog" the CPU or the thread's execution, preventing the event loop from moving to the next task.

• time.sleep(): Blocks the entire thread; the loop cannot "tick."

• requests.get() / urllib: Synchronous HTTP calls that wait for a network response without yielding.

• Heavy CPU Bound Tasks: Complex math, image processing, or large JSON parsing.

• Standard File I/O: `open().read()` is synchronous and can block if the disk is slow.

• Blocking Socket Calls: Any network call not wrapped in an `awaitable`.

2. How Blocking Code Affects Event Loop
When a synchronous function runs inside an `async` function, it occupies the single thread of the event loop. Because there is no `await` keyword to create a "yield point," the loop cannot pause the task. Every other task in the "Ready Queue" remains frozen until the blocking call returns.

3. Detection Strategy
• asyncio Debug Mode: Use `loop.set_debug(True)`. This monitors how long callbacks take.

• Slow Callback Threshold: Set `loop.slow_callback_duration = 0.1` to log warnings for any task taking longer than 100ms.

• Execution Monitors: Using `time.perf_counter()` in a background task to detect "heartbeat" gaps.

4. Key Insight
Async is not parallel. Calling a synchronous function inside an `async def` doesn't make it faster or "backgrounded"; it actually makes it more dangerous because it breaks the "cooperative" contract that the entire program relies on.

### Task Execution Patterns (The 3 Ways)
Understanding how you trigger a coroutine changes the flow of your program:

1. `await func()` (Sequential)

• Behavior: The calling function (e.g., `main()`) pauses completely and waits for `func()` to finish.

• Analogy: Standing at the counter waiting for your coffee. You don't do anything else until the cup is in your hand.

2. `asyncio.create_task(func())` (Background)

• Behavior: Schedules `func()` on the event loop and immediately moves to the next line of code.

• Analogy: Getting a buzzer at a cafe and sitting down to read. You are free to do other things while the coffee is being prepared.

• Warning: If the main program finishes, background tasks are terminated immediately, even if they aren't done.

3. `asyncio.gather(f1(), f2())` (Concurrent Grouping)

• Behavior: Starts multiple tasks at once and pauses the calling function until the entire group is finished.

• Analogy: Waiting at a table for a group order. You don't start the next activity until everyone's food has arrived.

| Feature | await func() | create_task(func()) | gather(f1(), f2()) |
|---------|--------------|---------------------|-------------------|
| Does main pause? | Yes, immediately. | No, it keeps going. | Yes, until all are done. |
| Execution | One after another. | Background/Concurrent. | Parallel-ish/Concurrent. |
| Result | Returns the value. | Returns a Task object. | Returns a list of values. |

- await func() (The "Stop and Wait" Approach)
When you use await, you are telling main() to pause completely until func() is finished.

```Python
async def main(): 
  print('Before func')
  await func()           # main() stops here for 2 seconds
  print('After func')    # This waits until func() returns

```
Behavior: Sequential.

Analogy: You go to a coffee shop, order a latte, and stand at the counter staring at the barista until it's done. You don't do anything else until you have that cup in your hand.

- asyncio.create_task(func()) (The "Fire and Forget" Approach)
This submits func() to the event loop's to-do list and immediately moves to the next line in main().

```Python
async def main(): 
  print('Before func')
  asyncio.create_task(func()) # Just puts func on the "To-Do" list
  print('After func')         # Runs IMMEDIATELY after the line above

```
Behavior: Concurrent/Background.

Analogy: You order your latte, the barista gives you a buzzer (the Task), and you immediately go sit down to read a book. You are "doing" two things: waiting for coffee and reading.

Crucial Note: If main() finishes before func(), the program might end before the task ever finishes!

- asyncio.gather(func()) (The "Group Order" Approach)
gather is used to run multiple things and wait for all of them to finish together.

```Python
async def main(): 
  print('Before func')
  await asyncio.gather(func(), another_func()) 
  print('After func') 
```
Behavior: Concurrent start, Sequential end.

Analogy: You and a friend order food. You wait at the table until both meals are ready before you start eating. It’s faster than ordering one after the other, but you still "pause" main() until the group is done.

| Code Pattern | Execution Style | Timeline |
|--------------|-----------------|----------|
| await f1()<br>await f2() | Sequential | f1 finishes ⮕ f2 starts |
| await gather(f1(), f2()) | Concurrent | f1 & f2 run in "parallel" ⮕ both finish ⮕ next line |

🏎️ Optimizing the Flow with gather
If func() contains steps that can happen at the same time, and main() has work it can do while func() is running, we use asyncio.gather.

```Python
import asyncio
import time

async def func():
    # By using gather here, these two sleeps overlap!
    # Total time for func: 1 second
    await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1)
    )
    print("Func finished its concurrent sleeps")

async def main():
    start = time.perf_counter()
    
    # We await func, then we await the final sleep
    await func()           # Takes 1 second
    await asyncio.sleep(1) # Takes 1 second
    
    end = time.perf_counter()
    print(f"Total Time: {end - start:.2f} seconds")

asyncio.run(main())

```

To finish the entire program in exactly 1 second, you would use asyncio.create_task or gather. If we use create_task, we "kick off" func and immediately move to the sleep in main.

Here is how you would write that, followed by the execution flow.

```Python

import asyncio
import time

async def func():
    # We await these concurrently (1s total)
    await asyncio.gather(asyncio.sleep(1), asyncio.sleep(1))
    print("Func finished")

async def main():
    start = time.perf_counter()
    
    # 1. Kick off func in the background
    task = asyncio.create_task(func()) 
    
    # 2. Immediately start the sleep in main
    await asyncio.sleep(1) 
    
    # 3. Ensure func is actually done before exiting
    await task 
    
    print(f"Total Time: {time.perf_counter() - start:.2f}s")

asyncio.run(main())

```

🕵️‍♂️ The Flow of Execution (The Background Pattern)

| Time | Action | Event Loop State |
|------|--------|------------------|
| 0.0s | create_task(func()) | func is added to the Ready Queue. It hasn't started yet! |
| 0.0s | await asyncio.sleep(1) | Yield Point! main pauses. The loop now looks at its queue. |
| 0.0s | func starts | The loop starts func. func hits its own gather(sleep, sleep). |
| 0.0s | Overlap | The loop now has three timers running for 1s (one from main, two from func). |
| 1.0s | Wake up | All timers expire at roughly the same time. |
| 1.0s | Cleanup | func finishes. main wakes up, hits await task (which is already done), and exits. |

Total Time: ~1.0 second.

📝 Cheat Sheet: Flow Control Summary

| Goal | Keyword | Result |
|------|---------|--------|
| Wait for it now | await func() | Code stops until func is finished. |
| Start it now, wait later | task = create_task(func()) | Code keeps running; you await task at the end. |
| Start many, wait for all | await gather(f1(), f2()) | All run together; code stops until the last one finishes. |

🧠 Your Final Mastery Question
Imagine you have a func() that doesn't have any await inside it (it just does a heavy math calculation for 1 second).

If you use create_task(func()) followed by await asyncio.sleep(1), will they still run concurrently in 1 second?

Yes, create_task always makes things run in the background.

No, because func doesn't yield control. It will block the loop for 1 second, and only after it's done will the sleep(1) start.

Total time would be 2 seconds.

Calling create_task is like putting a post-it note on the fridge. The "work" (the chef) doesn't even look at the post-it note until they finish what they are currently doing and reach a point where they can pause (an await).

The "Execution Handover"
Think of it as a relay race where there is only one runner (the CPU).

create_task(func()): You hand a baton to a second runner who is standing still. They don't start running yet.

print("Doing work"): The first runner keeps running.

await asyncio.sleep(0.1): The first runner stops and says, "I'm pausing."

The Loop: Only now does the Event Loop look at the "Ready Queue," see the second runner, and tell them, "Your turn! Go!"

🧪 The Proof: The "Immediate Print" Test
Look at this code. If create_task started immediately, you would see "Task Started" before "Main keeps going." But you won't.

```Python
async def my_task():
    print("2. Task Started")

async def main():
    print("1. About to create task")
    asyncio.create_task(my_task()) # Schedules it, but doesn't start it!
    
    print("3. Main keeps going...") 
    
    # Still hasn't started!
    await asyncio.sleep(0) # <--- THIS is where the loop switches to my_task
    print("4. Main is back")

asyncio.run(main())

```

Actual Output:

About to create task

Main keeps going...

Task Started

Main is back

In your example, the task starts running first, but only after main hits its await stop sign.

Here is the play-by-play of that exact moment when the CPU switches hands:

⏱️ The Switch Moment
The Setup: main calls create_task(func()). The loop puts func on the "To-Do" list. Nothing happens yet.

The Hand-off: main hits await asyncio.sleep(1).

main pauses and says to the Event Loop: "I'm waiting. You have control now."

The Decision: The Event Loop looks at its To-Do list. It sees func is ready to go.

The Execution: The loop starts running func immediately before it even starts the "sleep" timer for main.

The Chain Reaction: func runs until it hits an await (like its own asyncio.sleep).

The Idle State: Once both main and func are paused and waiting, the Event Loop finally sits back and waits for the timers to expire.

🎨 The "Baton Pass" Flow
main holds the baton.

main reaches an await. It drops the baton.

The Event Loop picks up the baton and hands it to func.

func runs until it hits an await, then drops the baton.

The Event Loop holds the baton while everyone waits for their timers.

what if main async operation ends first will the main exit?

This is the "cliffhanger" moment of async programming! The answer is yes, but with a very important consequence for your background task.

If main() reaches its final line and returns, the asyncio.run() call finishes, and the entire event loop shuts down. ### 🎬 The "Theater" Analogy Imagine main() is the Lead Actor in a play, and func() is a Stagehand cleaning up in the background.

The moment the Lead Actor finishes their final bow and the curtain closes (main returns), the theater lights are turned off immediately.

It doesn't matter if the Stagehand (func) was only halfway through their job. They are left in the dark and the show is over.

🕵️‍♂️ What happens to func()?
When main() exits first:

Sudden Death: The background task (func) is instantly terminated. It doesn't get a chance to finish its next line or even run a finally block in some cases.

The "Pending" Warning: You will often see a warning in your terminal:

RuntimeWarning: coroutine 'func' was never awaited OR Task was destroyed but it is pending!

Data Loss: If func was supposed to save data to a database or send an email, that work is lost.

🛡️ How to prevent the "Premature Exit"
If you want main to do its work but ensure func finishes before the program closes, you must explicitly join them at the end of main.

```Python

async def main():
    task = asyncio.create_task(func())
    
    await some_io_task_MAIN() # Main finishes this...
    
    print("Main is done with its work, now waiting for background task...")
    
    # 🛑 The "Anchor": Wait for the background task before leaving the theater
    await task

```

🧠 Summary for your Notes
The Rule: The lifecycle of the program is tied to the awaitable passed to asyncio.run() (usually main).

The Result: If the "root" task finishes, the loop stops, and all pending create_task jobs are killed.

The Fix: Always await your critical background tasks at the end of main if their completion is required.