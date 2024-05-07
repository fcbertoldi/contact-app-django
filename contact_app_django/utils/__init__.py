from django.conf import settings

from .form_renderers import HtmxFormMixin
from .models import TimestampedModel
from .tasks import send_task
from .views import HtmxDeleteView, HtmxDeletionMixin, HttpResponseSeeOther


def get_kvstore():
    from django.core.cache import caches

    return caches[settings.KVSTORE_ALIAS]


__all__ = [
    "HttpResponseSeeOther",
    "HtmxDeletionMixin",
    "HtmxDeleteView",
    "HtmxFormMixin",
    "TimestampedModel",
    "get_kvstore",
    "send_task",
]
