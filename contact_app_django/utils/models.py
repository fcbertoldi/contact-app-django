from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.updated = now
        if self.pk is None:
            self.created = now

        super().save(*args, **kwargs)

    def was_updated(self):
        return self.created != self.updated
