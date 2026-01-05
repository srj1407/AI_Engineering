import asyncio
import time

async def hello():
    print('Before sleep')
    await asyncio.sleep(2)
    print('After sleep')
    print('Done')

async def hello1():
    print('Before sleep1')
    await asyncio.sleep(2)
    print('After sleep1')
    print('Done1')

async def hello2():
    print('Before sleep2')
    await asyncio.sleep(2)
    print('After sleep2')
    print('Done2')

async def hello3():
    print('Before sleep')
    time.sleep(2)
    print('After sleep')
    print('Done')

def hello4():
    print('Before sleep')
    time.sleep(2)
    print('After sleep')
    print('Done')

async def hello5():
    print('Before sleep5')
    time.sleep(2)
    print('After sleep5')
    print('Done5')

async def hello6():
    print('Before sleep6')
    time.sleep(2)
    print('After sleep6')
    print('Done6')

async def main():
    start_time = time.time()
    print('Before hello')
    # await asyncio.gather(hello1(), hello2())
    # await hello()
    # await hello3()
    # hello4()
    await asyncio.gather(hello5(), hello6())
    print('After hello')
    end_time = time.time()
    print(f'Total_time: {end_time-start_time}')

asyncio.run(main())