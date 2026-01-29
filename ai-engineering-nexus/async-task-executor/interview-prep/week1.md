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

## Day 2 - Jan 28

### Problem 1: LeetCode 1115 - Print FooBar Alternately
- **Approach:** I used baton pass approach using baton_pass.wait() and baon_pass.set() approach.
- **Time Complexity:** O(1)
- **Key Learning:** Threading and Semaphore in python
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/print-foobar-alternately/description/)
- **Learning:**
1. Used baton pass approach in loop for executing loops alternatively.
2. Lock/Semaphore approach

- **Code Examples:**
```python

class FooBar:
    def __init__(self, n):
        self.n = n
        self.thread_1 = threading.Event()
        self.thread_2 = threading.Event()
        self.thread_1.set()

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            self.thread_1.wait()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.thread_2.set()
            self.thread_1.clear()

    def bar(self, printBar: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            self.thread_2.wait()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.thread_1.set()
            self.thread_2.clear()

```

```python

from threading import Lock
class FooBar:
    def __init__(self, n):
        self.n = n
        self.l1 = Lock() # Semaphore(1)
        self.l2 = Lock() # Semaphore(1)
        self.l2.acquire()

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.l1.acquire()
            printFoo()
            self.l2.release()

    def bar(self, printBar: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.l2.acquire()
            printBar()
            self.l1.release()

```

### Problem 2: LeetCode 238. Product of Array Except Self
- **Approach:** Storing prefix products in output array and sufix products in one variable.
- **Time Complexity:** O(n)
- **Time Complexity:** O(1)
- **Key Learning:** Manipulating arrays for prefix and suffix storing.
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/product-of-array-except-self/description/)

- **Code Examples:**
```CPP

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        vector<int> r(nums.size(), 1);
        int t=1;
        for(int i=1;i<nums.size();i++){
            r[i]=r[i-1]*nums[i-1];
        }
        for(int i=nums.size()-2;i>=0;i--){
            t*=nums[i+1];
            r[i]=r[i]*t;
        }
        return r;
    }
};


```

---

## Day 3 - Jan 29

### Problem 1: LeetCode 1116 - Print Zero Even Odd
- **Approach:** I used semaphore lock method with three locks for zero, even and odd.
- **Time Complexity:** O(n)
- **Key Learning:** Threading and Semaphore in python
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/print-zero-even-odd/description/)
- **Code Examples:**
```python

from threading import Lock

class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.z = Lock()
        self.e = Lock()
        self.o = Lock()
        self.e.acquire()
        self.o.acquire()
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(self.n):
            self.z.acquire()
            printNumber(0)
            if i % 2 == 0:
                self.o.release()
            else:
                self.e.release()
        
    def even(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(2, self.n+1, 2):
            self.e.acquire()
            printNumber(i)
            self.z.release()
        
    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(1, self.n+1, 2):
            self.o.acquire()
            printNumber(i)
            self.z.release()

```

### Problem 2: LeetCode 207 - Course Schedule
- **Approach:** Solving if all courses can be covered using indegree and queue.
- **Time Complexity:** Time complexity: O(V+E)
Processes every course (V) and every prerequisite (E) once.
- **Key Learning:** Think like this -> By taking indegree count first we are knowing how many individual islands are there. Then in each island we are going one by one using queue subtracting one from indegree when a prerequisite is covered.
- **Link:** [\[LeetCode link\]](https://leetcode.com/problems/course-schedule/description/)

- **Code Examples:**
```CPP

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<int> graph[2000];
        vector<int> indeg(numCourses, 0);
        int r=0;
        for(auto e: prerequisites){
            graph[e[1]].push_back(e[0]);
            indeg[e[0]]++;
        }
        queue<int> q;
        for(int i=0;i<numCourses;i++){
            if(indeg[i]==0){
                q.push(i);
            }
        }
        while(!q.empty()){
            int x=q.front();
            q.pop();
            r++;
            for(auto e: graph[x]){
                indeg[e]--;
                if(indeg[e]==0){
                    q.push(e);
                }
            }
        }
        return r==numCourses;
    }
};

```

---