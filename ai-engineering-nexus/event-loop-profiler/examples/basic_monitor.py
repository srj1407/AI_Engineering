import asyncio
from event_loop_profiler.monitor import EventLoopMonitor

async def fast_task():
    """Quick operation"""
    await asyncio.sleep(0.1)
    return "fast done"

async def medium_task():
    """Medium operation"""
    await asyncio.sleep(0.5)
    return "medium done"

async def slow_task():
    """Slow operation"""
    await asyncio.sleep(1.0)
    return "slow done"

async def main():
    monitor = EventLoopMonitor()
    
    tasks = [fast_task, medium_task, slow_task, fast_task]
    names = ["Fast-1", "Medium", "Slow", "Fast-2"]
    
    timeline = await monitor.run_with_monitoring(tasks, names)
    
    print(timeline.summary())

if __name__ == "__main__":
    asyncio.run(main())
