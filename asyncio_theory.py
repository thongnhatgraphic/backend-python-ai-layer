import asyncio
import time

async def worker1():
    return 1

async def main1():

    coro = worker1()

    task = asyncio.create_task(worker1())
    result = await coro

    print(task, result)
    print(result)

asyncio.run(main1())

# async def task1():
#     await asyncio.sleep(2)
#     print("Task 1 done")
# async def task2():
#     await asyncio.sleep(2)
#     print("Task 2 done")
# async def task3():
#     await asyncio.sleep(2)
#     print("Task 3 done")

# async def batch_job():
#     await task1() 
#     await task2() 
#     await task3()

# async def batch_job2():
#     await asyncio.gather(task1(), task2(), task3())

# asyncio.run(batch_job2())



# async def task3():
#     print("Task 3 start")
#     await asyncio.sleep(5)
#     print("Task 3 done")

# async def batch_job():
#     await asyncio.gather(task3(), task1(), task2())

# asyncio.run(batch_job())

# =====================================================
# ---------Asyncio with Create_task()---------------

async def worker():
    print("worker start")
    await asyncio.sleep(5)
    print("done")

async def main():

    
    asyncio.create_task(worker())

    print("continue")

    await asyncio.sleep(6)

    print("done main")

# asyncio.run(main())

async def worker():

    print("A")

    await asyncio.sleep(3)

    print("B")

async def main():

    task = asyncio.create_task(worker())

    await asyncio.sleep(2)

    print("Main")

    # await task

# asyncio.run(main())

# create_task() 1s
# send_notification() 5s
async def create_task():
    await asyncio.sleep(1)
    print("done create task")
async def send_notification():
    await asyncio.sleep(5)
    print("done send notification")

async def batch_job():
    await create_task()
    asyncio.create_task(send_notification(), name="send_notification")
    print("Done batch job")

# asyncio.run(batch_job())

# listener() print Listening...
# heartbeat() print Heartbeat...
async def listener():
    while True:
        await asyncio.sleep(1)
        print("Listening...")

async def heartbeat():
    while True:
        await asyncio.sleep(2)
        print("Heartbeat...")
async def simulate_ws():
    n = 0
    while True:
        print(f"Loop {n}")
        n += 1
        asyncio.create_task(listener())
        asyncio.create_task(heartbeat())
        await asyncio.sleep(10)

# asyncio.run(simulate_ws())

# async def task():
#     await asyncio.sleep(3)

# async def main():
#     start = time.time()

#     await task()

#     print(time.time() - start)

# asyncio.run(main())

async def create_task(): 
    await asyncio.sleep(1) 
    print("done create task") 
async def send_notification(): 
    await asyncio.sleep(5) 
    print("done send notification") 

async def batch_job(): 
    await create_task() 
    asyncio.create_task(send_notification()) 
    print("Done batch job")