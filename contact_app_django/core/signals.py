from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Contact


@receiver([post_save, post_delete], sender=Contact)
def on_contact_changed(sender, instance, **kwargs):
    from .services import archiver

    archiver.reset()
