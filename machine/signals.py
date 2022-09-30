from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=Profile)
def machine_type_save(sender, instance, **kwargs):
    instance.machine_type.add()


# post_save.connect(machine_type_save, sender=Profile)
