from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Подтверждение бронирования'
        message = 'Ваше бронирование подтверждено.'
        recipient_list = [instance.user.email]
        send_mail(subject, message, from_email=None, recipient_list=recipient_list)