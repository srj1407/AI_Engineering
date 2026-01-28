# Day 02: Async Task Executor - Data Models & Core Architecture

**Focus:** Python Fundamentals, Type Hints, Dataclasses, Async Concepts

---

1. What does a semaphore do? 🚦
A Semaphore is a synchronization primitive used to limit the number of concurrent tasks.

It maintains an internal counter (slots).

It acts like a bouncer: if the slots are full, new tasks must wait in a queue until an active task finishes and vacates a spot.

This is essential for preventing "resource exhaustion" (e.g., making 1,000 simultaneous API requests and getting blocked by a server).

A Semaphore 🚦 is best understood through real-world scenarios where access to a limited resource must be managed. Here are three distinct examples you can include in your day02.md notes to illustrate different use cases.

* The Database Connection Pool 🗄️
Most databases have a limit on how many people can talk to them at once. If 100 users try to save data at the exact same second, the database might crash.

The Setup: sem = asyncio.Semaphore(10)

The Logic: Even if your web server handles 1,000 requests, only 10 "slots" are available to talk to the database. The other 990 requests wait in a queue until a slot opens up.

* The Web Scraper (Rate Limiting) 🌐
If you crawl a website too fast, the site might think you are a "bot" and ban your IP address.

The Setup: sem = asyncio.Semaphore(3)

The Logic: You create a list of 50 URLs to download. By using the semaphore, your code only downloads 3 pages at a time. This keeps your traffic "low and slow" so you don't overwhelm the server.

* The "Mutex" (Mutual Exclusion) 🔒
This is a special case where the semaphore is set to exactly 1.

The Setup: sem = asyncio.Semaphore(1)

The Logic: Imagine two tasks trying to write to the same text file. If they both write at once, the text gets scrambled. A semaphore of 1 ensures Task A finishes writing and closes the file before Task B is allowed to start.

2. How does async with semaphore: work? 🔒
Using the async with statement is the recommended pattern because it acts as a Context Manager.

Automatic Acquisition: When the block starts, it automatically calls .acquire() to take a slot.

Guaranteed Release: Even if the code inside the block raises an error or crashes, the semaphore automatically calls .release() when the block exits.

Safety: This prevents "deadlocks" where slots are accidentally left "occupied" forever.

3. Why use Dataclasses vs. Regular Classes? 📦
Dataclasses (introduced in Python 3.7) are designed specifically for objects that primarily store data.

---

| Feature | Regular Class | Dataclass (@dataclass) |
|---------|---------------|------------------------|
| Boilerplate | You must write `__init__`, `__repr__`, etc. | Automatically generated for you |
| Readability | Can be cluttered with methods | Very clean; shows data fields and types |
| Comparison | Requires custom `__eq__` logic | Works out of the box (compares values) |
| Type Hints | Optional | Required (makes code more robust) |

---

### Real-World Use Cases of async-task-executor
- Running multiple API calls in parallel
- Batch processing with retry logic
- Background job execution
- Microservices task orchestration

---

## 🎯 Learning Objectives

1. **Dataclasses** - Modern Python data structures
2. **Type Hints** - Making code self-documenting and type-safe
3. **Async/Await** - Concurrent programming basics

---

**Key Concepts:**
- `Callable` - Type hint for any function
- `args/kwargs` - Store function parameters for later execution
- `field(default_factory=dict)` - Safely handle mutable defaults
- Default values make fields optional

---


**Key Concepts:**
- `Optional[Type]` - Value can be `None` or specified type
- Either `result` OR `error` will be set, never both
- Default values make all fields except `success` optional

---

## 📚 Key Concepts Learned

### Type Hints
- **Purpose:** Make code self-documenting and catch errors early
- **Basic types:** `str`, `int`, `float`, `bool`
- **Generic types:** `List[T]`, `Dict[K, V]`, `Optional[T]`
- **Special types:** `Callable`, `Any`

```python
# Without type hints (unclear)
def process(data):
    return data

# With type hints (clear)
def process(data: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in data}
```

### Dataclasses
- **Purpose:** Reduce boilerplate for data-holding classes
- **Auto-generates:** `__init__`, `__repr__`, `__eq__`
- **Benefits:** Cleaner code, less error-prone

```python
# Old way (verbose)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Dataclass way (concise)
@dataclass
class Point:
    x: float
    y: float
```

### Default Values in Dataclasses
- Fields with defaults must come **after** required fields
- Use `field(default_factory=...)` for mutable defaults (list, dict)

```python
@dataclass
class Example:
    name: str                              # Required
    tags: List[str] = field(default_factory=list)  # Optional with default
    count: int = 0                         # Optional with default
```

### Args and Kwargs
- **`*args`** - Capture positional arguments as tuple
- **`**kwargs`** - Capture keyword arguments as dictionary
- Used to pass variable arguments to functions

```python
def flexible_function(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

flexible_function(1, 2, 3, name="Alice", age=25)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 25}
```

---