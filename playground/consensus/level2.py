import asyncio
from random import random

LONG_MULT = 10
SHORT_MULT = 5
"""
Level Two -- Await infinite tasks (While True), without blocking on awaits
"""

async def long_task(input):
    while True:
        t = random() * LONG_MULT
        print("awaiting long task for {} sec".format(t))
        await asyncio.sleep(3)
        print("long task done: {}".format(input ** 2))

async def short_task(input):
    while True:
        t = random() * SHORT_MULT
        await asyncio.sleep(1)
        print("awaiting short task for {} sec".format(t))
        print("short task done: {}".format(input // 2))


loop = asyncio.get_event_loop()
# loop.create_task(long_task)

loop.run_until_complete(asyncio.gather(long_task(4), long_task(8), short_task(12), ))


# async def coro(tag):
#     print(">", tag)
#     await asyncio.sleep(random.uniform(0.5, 5))
#     print("<", tag)
#     return tag
#
#
# loop = asyncio.get_event_loop()
#
# tasks = [coro(i) for i in range(1, 11)]
#
# print("Get first result:")
# finished, unfinished = loop.run_until_complete(
#     asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
#
# for task in finished:
#     print(task.result())
# print("unfinished:", len(unfinished))
#
# print("Get more results in 2 seconds:")
# finished2, unfinished2 = loop.run_until_complete(
#     asyncio.wait(unfinished, timeout=2))
#
# for task in finished2:
#     print(task.result())
# print("unfinished2:", len(unfinished2))
#
# print("Get all other results:")
# finished3, unfinished3 = loop.run_until_complete(asyncio.wait(unfinished2))
#
# for task in finished3:
#     print(task.result())
#
# loop.close()