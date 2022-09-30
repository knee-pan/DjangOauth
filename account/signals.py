from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from models import User


@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender, instance, **kwargs):
    """
    before saved in the db
    """
    print(instance.id)
    instance.save()


@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    """
    after saved in the db
    """
    if created:
        print("New user created", instance.username)
        instance.save()
    else:
        print(instance.username, "was just saved")
