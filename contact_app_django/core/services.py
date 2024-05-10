import enum
import time
from io import BytesIO
from threading import Condition, Lock, Thread

from django.core import serializers


class ArchiverException(Exception):
    pass


class Status(enum.Enum):
    WAITING = enum.auto()
    RUNNING = enum.auto()
    COMPLETE = enum.auto()


class Archiver:
    def __init__(self) -> None:
        self.progress = 0
        self._status = Status.WAITING
        self._lock = Lock()
        self._cond = Condition()
        self.thread = None

    @classmethod
    def create(cls):
        archiver = Archiver()
        archiver.thread = Thread(target=archiver._run)
        archiver.thread.start()
        return archiver

    @property
    def status(self):
        with self._lock:
            return self._status

    @status.setter
    def status(self, value: Status):
        with self._lock:
            self._status = value

    def archive(self):
        with self._lock:
            if self._status != Status.RUNNING:
                self._status = Status.RUNNING
        with self._cond:
            self._cond.notify()

    def running(self) -> bool:
        return self.status != Status.RUNNING

    def _run(self):
        from django.db import close_old_connections

        close_old_connections()

        while True:
            with self._cond:
                self._cond.wait_for(self.running)

            self._archive_task()
            close_old_connections()

    def _archive_task(self):
        self.progress = 0
        num_steps = 5
        for i in range(num_steps):
            time.sleep(1)
            if self.status != Status.RUNNING:
                return

            self.progress += 1 / num_steps

        self.status = Status.COMPLETE

    def get_archive_file(self):
        from .models import Contact

        if self.status != Status.COMPLETE:
            raise ArchiverException("Archive file not available")

        self.status = Status.WAITING
        data = serializers.serialize("json", Contact.objects.all())
        return BytesIO(data.encode())

    def reset(self):
        with self._lock:
            if self._status == Status.RUNNING:
                self._status = Status.WAITING
                self.progress = 0.0


archiver = Archiver.create()
