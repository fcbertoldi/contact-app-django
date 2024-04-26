import uuid
from typing import Optional
from django.db import models
from django.db.models import Q


class ContactManager(models.Manager):
    def search(self, search_param: Optional[str]):
        if search_param is None:
            return self.none()

        return self.get_queryset().filter(
            Q(first__icontains=search_param)
            | Q(last__icontains=search_param)
            | Q(email__icontains=search_param)
            | Q(phone__icontains=search_param)
        )


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

    objects = ContactManager()

    def __str__(self):
        return " ".join([self.first, self.last])
