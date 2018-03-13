"""
LEVEL 3 -- Create a networking class that uses ZMQ to subscribe to operations, do some short processing
on them, and print

For now, just subscribe to 1 URL
"""

from cilantro.logger import get_logger
from random import random
import time

import asyncio
import zmq
import zmq.asyncio

URL = "tcp://127.0.0.1:5566"

class Sub():
    def __init__(self, url="tcp://127.0.0.1:5566"):
        self.url = url
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(socket_type=zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.socket.connect(self.url)

        self.loop = asyncio.get_event_loop()
        # THIS WILL BLOCK
        # self.loop.run_until_complete(self.listen())
        # asyncio.ensure_future(self.test())
        # asyncio.ensure_future(self.listen())

        self.loop.run_until_complete(self.listen())

        print("i am unblocked!")

    async def test(self):
        print("test starting...")
        await asyncio.sleep(0.5)
        print("test done")

    async def listen(self):
        print("Starting listening...")
        while True:
            print("sub waiting...")
            # msg = self.socket.recv()
            msg = await self.socket.recv()
            print("sub got msg: {}".format(msg))



if __name__ == "__main__":
    sub = Sub()

    time.sleep(16)

    print("done")