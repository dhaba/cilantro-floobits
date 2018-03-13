import asyncio
import zmq
import zmq.asyncio
import aioprocessing
from multiprocessing import Process, Queue
from threading import Thread
from cilantro.logger import get_logger
from random import random
import time


URL = "tcp://127.0.0.1:5566"


class Command:

    SUB, UNSUB, UNSUB_ALL = range(3)

    def __init__(self, cmd, **kwargs):
        self.type = cmd
        self.kwargs = kwargs
        # TODO -- validate cmd and kwargs with assertions (should not have any hardcore validation irl, i dont think?
        # b/c there would be overhead, and it might now be an attack vecotr idk

    def __repr__(self):
        return "cmd={}, {}".format(self.type, self.kwargs)


class NetworkReactor(Thread):

    def __init__(self, queue):
        super().__init__()
        self.log = get_logger("Reactor")
        self.queue = queue

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.ctx, self.socket, self.futures = None, None, []

    def run(self):
        super().run()
        self.log.debug("\n\n\nRun started")

        self.ctx = zmq.asyncio.Context()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(asyncio.gather(self.read_queue(),))

    async def read_queue(self):
        self.log.warning("-- Starting Queue Listening --")
        while True:
            self.log.debug("Reading queue...")

            cmd = await self.queue.coro_get()
            assert type(cmd) == Command, "Only a Command object can be inserted into the queue"
            self.log.info("Got data from queue: {}".format(cmd))
            self.execute(cmd)

    def execute(self, cmd: Command):
        self.log.info("Executing command: {}".format(cmd))
        if cmd.type == Command.SUB:
            self.socket = self.ctx.socket(socket_type=zmq.SUB)
            self.socket.setsockopt(zmq.SUBSCRIBE, b'')
            self.socket.connect(URL)

            # TAKE 1
            time.sleep(0.2)
            future = asyncio.ensure_future(self.receive(self.socket))
            self.log.critical("Appending future: {}".format(future))
            self.futures.append(future)

            # TAKE 2 -- with create_task

        else:
            self.log.error("Unknown command type: {}".format(cmd))
            raise NotImplementedError("Unknown command type: {}".format(cmd))

    async def receive(self, socket):
        # could just use self.socket here
        self.log.warning("--- Starting Receiving ----")
        while True:
            self.log.info("waiting for msg...")
            msg = await socket.recv()
            self.log.info("got msg: {}".format(msg))


def sillify(string):
    return "~0.0~  xD   o->    {}   <-o    xD  ~0.0~".format(string)


if __name__ == "__main__":
    log = get_logger("Main")
    q = aioprocessing.AioQueue()
    reactor = NetworkReactor(queue=q)
    reactor.start()

    # q.coro_put("Hi This Is An Item")
    # q.coro_put("balls")

    q.coro_put(Command(Command.SUB, arg1='hello', arg2='world'))


    # async def listen(self):
    #     self.log.debug("-- Starting Listening --")
    #     self.socket = self.ctx.socket(socket_type=zmq.SUB)
    #     self.socket.setsockopt(zmq.SUBSCRIBE, b'')
    #     self.socket.connect(URL)
    #     while True:
    #         self.log.debug("listen waiting...")
    #         msg = await self.socket.recv()
    #         self.log.debug("listen got msg: {}".format(msg))