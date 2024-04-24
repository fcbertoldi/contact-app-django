import uuid
from django.db import models


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]
