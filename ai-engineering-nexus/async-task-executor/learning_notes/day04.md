# 📚 Comprehensive Notes: Asyncio Reliability & Retries

## 1. Asyncio Timeout Handling ⏱️

Timeouts prevent your application from hanging indefinitely when external resources (APIs, databases) are slow.

### `asyncio.wait_for(aw, timeout)`

- **Behavior**: Wraps a single awaitable. If the `timeout` (in seconds) expires, it raises `asyncio.TimeoutError`.
- **Cancellation**: Crucially, it automatically cancels the underlying task. This stops the task from wasting resources after you've given up on it.
- **Cleanup**: Use `try...finally` blocks within your coroutines to ensure resources (like database connections or open files) are closed properly if a cancellation occurs.

#### Code Example:

```python
import asyncio

async def fetch_data():
    """Simulates a slow API call"""
    await asyncio.sleep(5)  # Simulates 5 second delay
    return "Data fetched"

async def main():
    try:
        # Wait maximum 2 seconds for the operation
        result = await asyncio.wait_for(fetch_data(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out!")

# Run the example
asyncio.run(main())
```

#### With Proper Cleanup:

```python
import asyncio

async def fetch_with_cleanup():
    """Demonstrates proper resource cleanup"""
    connection = None
    try:
        # Simulate opening a connection
        connection = "Database Connection"
        print(f"Opened: {connection}")
        
        # Long running operation
        await asyncio.sleep(10)
        return "Data"
    finally:
        # This runs even if cancelled
        if connection:
            print(f"Closed: {connection}")

async def main():
    try:
        result = await asyncio.wait_for(fetch_with_cleanup(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out, but cleanup still happened!")

asyncio.run(main())
```

---

### `asyncio.timeout(delay)` (Python 3.11+)

- **Style**: A context manager used with `async with`.
- **Usage**: Best for wrapping a block of multiple asynchronous statements rather than just one function call.

#### Code Example:

```python
import asyncio

async def multiple_operations():
    """Demonstrates timeout for multiple operations"""
    try:
        async with asyncio.timeout(5.0):
            # Multiple async operations within the timeout
            await asyncio.sleep(1)
            print("First operation complete")
            
            await asyncio.sleep(2)
            print("Second operation complete")
            
            await asyncio.sleep(3)  # This will cause timeout
            print("Third operation complete")
    except TimeoutError:
        print("One or more operations timed out!")

asyncio.run(multiple_operations())
```

---

## 2. Exponential Backoff & Jitter 📈

When a request fails, retrying immediately can lead to a "retry storm" that overwhelms a struggling server.

### The Exponential Backoff Formula

The delay increases exponentially with each failed attempt to give the system time to recover.

$$delay = base \times 2^{attempt}$$

(Where attempt usually starts at 0)

**Example (Base = 0.5s):**
- Attempt 0: $0.5 \times 2^0 = 0.5s$
- Attempt 1: $0.5 \times 2^1 = 1.0s$
- Attempt 2: $0.5 \times 2^2 = 2.0s$
- Attempt 3: $0.5 \times 2^3 = 4.0s$

#### Code Example - Basic Exponential Backoff:

```python
import asyncio

async def unstable_api_call():
    """Simulates an unreliable API"""
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("API Error")
    return "Success!"

async def retry_with_backoff(max_retries=5, base_delay=0.5):
    """Retry with exponential backoff"""
    for attempt in range(max_retries):
        try:
            result = await unstable_api_call()
            print(f"✓ Success on attempt {attempt + 1}")
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"✗ Failed after {max_retries} attempts")
                raise
            
            # Calculate exponential backoff delay
            delay = base_delay * (2 ** attempt)
            print(f"✗ Attempt {attempt + 1} failed. Retrying in {delay}s...")
            await asyncio.sleep(delay)

asyncio.run(retry_with_backoff())
```

---

### The Role of Jitter 🎲

If 1,000 clients fail at once and use the exact same formula, they will all retry at the exact same moment, creating "spikes" of traffic. Jitter adds randomness to break this synchronization.

- **Full Jitter**: `random.uniform(0, delay)`
- **Benefit**: Spreads the load evenly over time, allowing the server to process requests more smoothly.

#### Code Example - Exponential Backoff with Jitter:

```python
import asyncio
import random

async def retry_with_jitter(max_retries=5, base_delay=0.5):
    """Retry with exponential backoff and full jitter"""
    for attempt in range(max_retries):
        try:
            result = await unstable_api_call()
            print(f"✓ Success on attempt {attempt + 1}")
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"✗ Failed after {max_retries} attempts")
                raise
            
            # Calculate base delay with exponential backoff
            base = base_delay * (2 ** attempt)
            
            # Apply full jitter
            delay = random.uniform(0, base)
            
            print(f"✗ Attempt {attempt + 1} failed. Retrying in {delay:.2f}s...")
            await asyncio.sleep(delay)

asyncio.run(retry_with_jitter())
```

#### Comparison - Multiple Clients Without Jitter:

```python
import asyncio
import time

async def client_without_jitter(client_id, base_delay=1.0):
    """Simulates client retrying without jitter"""
    for attempt in range(3):
        delay = base_delay * (2 ** attempt)
        print(f"Client {client_id}: Retry at {time.time():.2f}")
        await asyncio.sleep(delay)

async def demo_without_jitter():
    """All clients retry at the same time - BAD!"""
    await asyncio.gather(*[
        client_without_jitter(i) for i in range(5)
    ])

# Notice all clients retry at exactly the same moments
asyncio.run(demo_without_jitter())
```

#### With Jitter - Traffic is Distributed:

```python
import asyncio
import random
import time

async def client_with_jitter(client_id, base_delay=1.0):
    """Simulates client retrying with jitter"""
    for attempt in range(3):
        base = base_delay * (2 ** attempt)
        delay = random.uniform(0, base)
        print(f"Client {client_id}: Retry at {time.time():.2f}")
        await asyncio.sleep(delay)

async def demo_with_jitter():
    """Clients retry at different times - GOOD!"""
    await asyncio.gather(*[
        client_with_jitter(i) for i in range(5)
    ])

# Notice clients retry at different, distributed moments
asyncio.run(demo_with_jitter())
```

---

## 3. Throttling with Semaphores 🚦

While timeouts and retries handle reliability, semaphores handle capacity.

- **`asyncio.Semaphore(value)`**: Limits the number of concurrent tasks allowed to enter a specific section of code.
- **Implementation**: `async with my_semaphore:` ensures that even if you have 100 tasks, only `value` tasks run the protected code simultaneously.

#### Code Example - Basic Semaphore:

```python
import asyncio

async def access_resource(semaphore, task_id):
    """Simulates accessing a limited resource"""
    async with semaphore:
        print(f"Task {task_id}: Accessing resource")
        await asyncio.sleep(2)  # Simulate work
        print(f"Task {task_id}: Releasing resource")

async def main():
    # Only allow 3 concurrent accesses
    semaphore = asyncio.Semaphore(3)
    
    # Create 10 tasks, but only 3 will run at a time
    tasks = [access_resource(semaphore, i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

#### Code Example - Rate Limiting API Calls:

```python
import asyncio
import time

async def call_api(semaphore, url_id):
    """Simulates an API call with rate limiting"""
    async with semaphore:
        print(f"{time.time():.2f}: Calling API {url_id}")
        await asyncio.sleep(1)  # Simulate API response time
        return f"Response from {url_id}"

async def main():
    # Limit to 5 concurrent API calls
    api_semaphore = asyncio.Semaphore(5)
    
    # Make 20 API calls, but max 5 at a time
    tasks = [call_api(api_semaphore, i) for i in range(20)]
    results = await asyncio.gather(*tasks)
    
    print(f"\nReceived {len(results)} responses")

asyncio.run(main())
```

---

## 4. Implementation Summary - Complete Resilient Function 🛡️

A resilient async function typically combines all these patterns:

1. **Semaphore** to limit total concurrent hits
2. **Retry Loop** to handle transient failures
3. **Timeout** inside the loop to cap each individual attempt
4. **Exponential Backoff + Jitter** to wait between retries

### Complete Example:

```python
import asyncio
import random
from typing import Any

class ResilientAPIClient:
    def __init__(self, max_concurrent=5, max_retries=3, base_delay=1.0, timeout=10.0):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.timeout = timeout
    
    async def fetch(self, url: str) -> Any:
        """
        Resilient fetch with:
        - Semaphore for concurrency control
        - Retry logic with exponential backoff and jitter
        - Timeout for each attempt
        """
        async with self.semaphore:  # 1. Limit concurrency
            for attempt in range(self.max_retries):  # 2. Retry loop
                try:
                    # 3. Timeout for this attempt
                    result = await asyncio.wait_for(
                        self._make_request(url),
                        timeout=self.timeout
                    )
                    print(f"✓ Success fetching {url}")
                    return result
                    
                except (asyncio.TimeoutError, Exception) as e:
                    if attempt == self.max_retries - 1:
                        print(f"✗ Failed fetching {url} after {self.max_retries} attempts")
                        raise
                    
                    # 4. Exponential backoff with jitter
                    base = self.base_delay * (2 ** attempt)
                    delay = random.uniform(0, base)
                    
                    print(f"⚠ Attempt {attempt + 1} failed for {url}. "
                          f"Retrying in {delay:.2f}s... (Error: {e})")
                    await asyncio.sleep(delay)
    
    async def _make_request(self, url: str) -> str:
        """Simulates actual HTTP request (replace with real implementation)"""
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Simulate 30% failure rate
        if random.random() < 0.3:
            raise Exception("Network error")
        
        return f"Data from {url}"


async def main():
    client = ResilientAPIClient(
        max_concurrent=3,    # Max 3 concurrent requests
        max_retries=3,       # Retry up to 3 times
        base_delay=0.5,      # Start with 0.5s delay
        timeout=5.0          # 5s timeout per attempt
    )
    
    # Fetch from multiple URLs
    urls = [f"https://api.example.com/endpoint/{i}" for i in range(10)]
    
    try:
        results = await asyncio.gather(*[
            client.fetch(url) for url in urls
        ], return_exceptions=True)
        
        # Process results
        successes = [r for r in results if not isinstance(r, Exception)]
        failures = [r for r in results if isinstance(r, Exception)]
        
        print(f"\n{'='*50}")
        print(f"Successful: {len(successes)}")
        print(f"Failed: {len(failures)}")
        
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Example - With Metrics:

```python
import asyncio
import random
import time
from dataclasses import dataclass
from typing import List

@dataclass
class RequestMetrics:
    url: str
    attempts: int
    total_time: float
    success: bool

class MetricsAPIClient(ResilientAPIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics: List[RequestMetrics] = []
    
    async def fetch(self, url: str) -> Any:
        start_time = time.time()
        attempts = 0
        success = False
        
        try:
            async with self.semaphore:
                for attempt in range(self.max_retries):
                    attempts = attempt + 1
                    try:
                        result = await asyncio.wait_for(
                            self._make_request(url),
                            timeout=self.timeout
                        )
                        success = True
                        return result
                    except (asyncio.TimeoutError, Exception) as e:
                        if attempt == self.max_retries - 1:
                            raise
                        base = self.base_delay * (2 ** attempt)
                        delay = random.uniform(0, base)
                        await asyncio.sleep(delay)
        finally:
            total_time = time.time() - start_time
            self.metrics.append(RequestMetrics(
                url=url,
                attempts=attempts,
                total_time=total_time,
                success=success
            ))
    
    def print_metrics(self):
        print(f"\n{'='*60}")
        print("REQUEST METRICS")
        print(f"{'='*60}")
        
        total = len(self.metrics)
        successful = sum(1 for m in self.metrics if m.success)
        
        print(f"Total Requests: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {total - successful} ({(total-successful)/total*100:.1f}%)")
        
        avg_time = sum(m.total_time for m in self.metrics) / total
        avg_attempts = sum(m.attempts for m in self.metrics) / total
        
        print(f"Average Time: {avg_time:.2f}s")
        print(f"Average Attempts: {avg_attempts:.2f}")
        print(f"{'='*60}")


async def main_with_metrics():
    client = MetricsAPIClient(
        max_concurrent=3,
        max_retries=3,
        base_delay=0.5,
        timeout=5.0
    )
    
    urls = [f"https://api.example.com/endpoint/{i}" for i in range(15)]
    
    results = await asyncio.gather(*[
        client.fetch(url) for url in urls
    ], return_exceptions=True)
    
    client.print_metrics()

if __name__ == "__main__":
    asyncio.run(main_with_metrics())
```

---

## Key Takeaways 🎯

1. **Always use timeouts** to prevent hanging operations
2. **Implement retries** with exponential backoff for transient failures
3. **Add jitter** to prevent thundering herd problems
4. **Use semaphores** to control concurrency and prevent overwhelming resources
5. **Combine all patterns** for production-ready resilient systems
6. **Monitor and measure** with metrics to understand system behavior

---

## Common Pitfalls to Avoid ⚠️

1. **No timeout**: Your app hangs forever waiting for slow resources
2. **No jitter**: All clients retry simultaneously, creating traffic spikes
3. **No semaphore**: Too many concurrent requests overwhelm your system or the remote API
4. **Infinite retries**: Failed operations retry forever, wasting resources
5. **No cleanup**: Resources leak when operations are cancelled
6. **Ignoring exceptions**: Silent failures make debugging impossible

---

## Further Reading 📖

- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [AWS Architecture Blog - Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google Cloud - Retry Pattern](https://cloud.google.com/architecture/error-handling)