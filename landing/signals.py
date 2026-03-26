from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactRequest
from .telegram import send_new_request_notification


@receiver(post_save, sender=ContactRequest)
def contactrequest_created(sender, instance, created, **kwargs):
    # send notification on creation
    if created:
        try:
            send_new_request_notification(instance.id)
        except Exception:
            pass
