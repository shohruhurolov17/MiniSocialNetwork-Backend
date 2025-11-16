from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.users.models import CustomUser
from django.core.mail import send_mail
from apps.users.tasks import send_verification_url_to_email


@receiver(post_save, sender=CustomUser)
def create_user(sender, instance, created, **kwargs):

    if created:

        send_verification_url_to_email.apply_async([
            instance.email,
            instance.id
        ])

