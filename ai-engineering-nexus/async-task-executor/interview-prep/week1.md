## Day 1 - Jan 27

### Problem 1: LeetCode 1114 - Print in Order
- **Approach:** I used baton pass approach using baton_pass.wait() and baon_pass.set() approach.
- **Time Complexity:** O(1)
- **Key Learning:** Threading in python
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/print-in-order/)
- **Learning:**
Python Threading
1. What is Threading? 🧵Threading allows a single program to run multiple threads (smaller units of execution) concurrently.
Best for: I/O-bound tasks (network requests, reading files, user input).
Managed by: The Operating System (OS) decides when to switch between threads.
2. The Global Interpreter Lock (GIL) 🔒The GIL is a "one-at-a-time" lock in Python.It prevents multiple threads from executing Python code simultaneously on different CPU cores.Result: Threading provides concurrency (switching fast), but not true parallelism for CPU-heavy math.
3. Key Synchronization Tools 🚦ToolPurposeAnalogy.start()Begins the thread's execution.Sending a runner onto the track. 🏃‍♂️.join()Makes the main program wait for the thread to finish.Waiting at the finish line for the runner. 🏁Event()A signal one thread sends to another to "go" or "wait".A relay race baton pass. 🤝Lock()Ensures only one thread can access a variable at a time.A single bathroom key in a coffee shop. 🔑
4. Sequencing vs. Concurrency 🔄Sequential: start() -> join() -> start() -> join(). (One after another).Concurrent: start() all -> join() all at the end. (All running at once).
5. Moving to the Relay Race Logic 🧠To answer your earlier question about the "Baton Pass" approach:If Task 1 forgets to call self.baton_1_to_2.set(), Task 2 will sit at the self.baton_1_to_2.wait() line forever. Because Task 2 is stuck waiting, it never calls self.baton_2_to_3.set(), meaning Task 3 also waits forever. This is a common type of "hang" in multi-threaded programs.

- **Code Examples:**
```python

import threading
import time

def task(name):
    print(f"Task {name} is running...")
    time.sleep(1)
    print(f"Task {name} is done!")

# Create the threads
t1 = threading.Thread(target=task, args=("1",))
t2 = threading.Thread(target=task, args=("2",))
t3 = threading.Thread(target=task, args=("3",))

# Execute in sequence
t1.start()
t1.join()  # Main program pauses until t1 is finished

t2.start()
t2.join()  # Main program pauses until t2 is finished

t3.start()
t3.join()  # Main program pauses until t3 is finished

print("All tasks completed in order.")

```

```python

class Foo:
    def __init__(self):
        self.baton_passed_1_to_2 = threading.Event()
        self.baton_passed_2_to_3 = threading.Event()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.baton_passed_1_to_2.set()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        
        # printSecond() outputs "second". Do not change or remove this line.
        self.baton_passed_1_to_2.wait()
        printSecond()
        self.baton_passed_2_to_3.set()


    def third(self, printThird: 'Callable[[], None]') -> None:
        
        # printThird() outputs "third". Do not change or remove this line.
        self.baton_passed_2_to_3.wait()
        printThird()

```

### Problem 2: 26. Remove Duplicates from Sorted Array
- **Approach:** Using two pointers i and j. j remains behind and replacesmthe new unique element found by i.
- **Time Complexity:** O(n)
- **Key Learning:** Two pointers
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=problem-list-v2&envId=array)

- **Code Examples:**

```CPP
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int i=1, j=1;
        while(i<nums.size()){
            if(nums[i]==nums[i-1]){
                i++;
            }
            else{
                nums[j]=nums[i];
                j++;
                i++;
            }
        }
        return j;

    }
};

```
---