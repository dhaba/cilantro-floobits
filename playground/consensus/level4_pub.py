from cilantro.logger import get_logger
import zmq
import asyncio
from random import random

from multiprocessing import Process

URL = "tcp://127.0.0.1:5566"

class NetworkManager(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.log = get_logger("NetworkingManager")
        self.ctx = zmq.Context()

        self.socket = self.ctx.socket(socket_type=zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.socket.connect(self.url)

        self.loop = asyncio.get_event_loop()
        # THIS WILL BLOCK
        self.loop.run_until_complete(self.listen())

        self.log.debug("i am unblocked!")

    async def listen(self):
        self.log.debug("Starting listening...")
        while True:
            self.log.debug("waiting for msg...")
            msg = self.socket.recv()
            self.log.debug("got msg: {}".format(msg))

class Sub():
    def __init__(self, url="tcp://127.0.0.1:5566"):
        self.url = url
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(socket_type=zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.socket.connect(self.url)

        self.loop = asyncio.get_event_loop()
        # THIS WILL BLOCK
        self.loop.run_until_complete(self.listen())

        print("i am unblocked!")

    async def listen(self):
        print("Starting listening...")
        while True:
            print("sub waiting...")
            msg = self.socket.recv()
            print("sub got msg: {}".format(msg))


if __name__ == "__main__":
    print("starting listening...")
    sub = Sub()
    print("done")

