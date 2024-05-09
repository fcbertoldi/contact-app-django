import queue
from multiprocessing import Queue
from multiprocessing.pool import ThreadPool

_task_queue = None


class TaskQueue:
    def __init__(self, archiver):
        self._worker_queue = Queue(maxsize=1)
        self._worker_pool = ThreadPool(
            processes=1, initializer=self._run, initargs=(self._worker_queue, archiver)
        )

    def enqueue(self, **kwargs):
        try:
            self._worker_queue.put_nowait(kwargs)
        except queue.Full:
            print("Queue is full")

    def _run(self, worker_queue: Queue, archiver):
        from django.db import close_old_connections

        close_old_connections()

        while True:
            _ = worker_queue.get()
            archiver.do_run()
            close_old_connections()


def enqueue(**kwargs):
    _task_queue.enqueue(**kwargs)


def init(archiver):
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue(archiver)
