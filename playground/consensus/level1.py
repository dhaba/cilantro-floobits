import asyncio
from random import random
from cilantro.logger import get_logger
"""
Level one -- Await n long running tasks concurrently 
"""

async def long_task(input):
    t = random() * 4
    print("awaiting long task for {} sec".format(t))
    await asyncio.sleep(t)
    print("long task done: {}".format(input ** 2))

async def short_task(input):
    t = random()
    print("awaiting short task for {} sec".format(t))
    print("short task done: {}".format(input // 2))


loop = asyncio.get_event_loop()
# loop.create_task(long_task)

loop.run_until_complete(asyncio.gather(long_task(4), long_task(8), short_task(12), ))

# loop.close()

