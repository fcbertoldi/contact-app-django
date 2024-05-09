import enum
import time
from io import StringIO
from threading import Lock

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

    @property
    def status(self):
        with self._lock:
            return self._status

    @status.setter
    def status(self, value: Status):
        with self._lock:
            self._status = value

    def run(self):
        from contact_app_django.tasks import enqueue

        if self.status != Status.RUNNING:
            enqueue()

    def do_run(self):
        self.status = Status.RUNNING
        self.progress = 0
        for i in range(5):
            time.sleep(1)
            if self.status != Status.RUNNING:
                return

            self.progress += 20

        self.status = Status.COMPLETE

    def get_archive_file(self):
        from .models import Contact

        if self.status != Status.COMPLETE:
            raise ArchiverException("Archive file not available")

        data = serializers.serialize("json", Contact.objects.all())
        return StringIO(initial_value=data)

    def reset(self):
        with self._lock:
            if self._status == Status.RUNNING:
                self._status = Status.WAITING
                self.progress = 0.0


archiver = Archiver()
