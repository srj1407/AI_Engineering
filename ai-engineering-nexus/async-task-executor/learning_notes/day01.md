📝 Learning Notes: Day 01 - Async Fundamentals

1. What is a coroutine? 🧬
A coroutine is a specialized version of a Python function defined with async def. Unlike a regular function that runs to completion the moment it's called, a coroutine:

Returns a coroutine object when called. 📦

Requires an Event Loop (via asyncio.run()) to actually execute.

Can "pause" its execution to let other code run.

2. What does await actually do? ⏸️
The await keyword is a signal to the Event Loop. It says: "I am waiting for this specific task to finish. While I wait, you are free to go run other tasks."

It can only be used inside an async function.

It effectively "unblocks" the execution thread.

3. Blocking vs. Non-blocking 🧱  

    | Feature                       | Blocking (time.sleep)                           | Non-blocking (asyncio.sleep)                  |
    |-------------------------------|--------------------------------------------------|------------------------------------------------|
    | Execution                     | Stops the entire program.                        | Pauses only the current task.                  |
    | Event Loop                    | "Freezes" the loop; nothing else moves.        | Allows the loop to switch tasks.               |
    | Analogy                      | Waiting for the kettle to boil before doing anything else. | Starting the kettle, then cleaning a dish while it heats up. |

4. import asyncio -> Importing async library

5. 