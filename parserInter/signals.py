from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_email

@receiver(post_save, sender=Order)
def order_status_update(sender, instance, **kwargs):
    if instance.confirmed == True:
        if instance.status == 'pending' or instance.status == 'confirmed' or instance.status == 'finished':
            send_email(instance)
