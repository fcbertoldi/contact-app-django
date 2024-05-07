import queue
from multiprocessing import Queue
from multiprocessing.pool import ThreadPool


def _task_impl(**kwargs):
    from contact_app_django.core.models import Contact

    print(f"Task: {kwargs}")
    num_contacts = Contact.objects.count()
    print(f"Contact count: {num_contacts}")


def _worker(worker_queue: Queue):
    from django.db import close_old_connections

    close_old_connections()

    while True:
        task_kwargs = worker_queue.get()
        _task_impl(**task_kwargs)
        close_old_connections()


def send_task(**kwargs):
    try:
        worker_queue.put_nowait(kwargs)
    except queue.Full:
        print("Queue is full")


worker_queue = Queue(maxsize=1)
worker_pool = ThreadPool(processes=1, initializer=_worker, initargs=(worker_queue,))
