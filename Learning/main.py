from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

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

@app.get("/health")
async def read_root():
    start_time = time.time()
    print('Before hello')
    await asyncio.gather(hello1(), hello2())
    print('After hello')
    end_time = time.time()
    print(f'Total_time: {end_time-start_time}')
    return {"Total_time": end_time-start_time}
