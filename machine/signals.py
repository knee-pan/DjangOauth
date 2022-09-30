from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver

from .models import MachineType, Profile


@receiver(post_save, sender=Profile)
def profile_mType_save(sender, instance, **kwargs):
    instance.machine_type.add()


# post_save.connect(machine_type_save, sender=Profile)


@receiver(pre_delete, sender=MachineType)
def machine_type_pre_delete(sender, instance, created, **kwargs):
    # move or make back up of this data
    print(instance.id, "will be remove")


@receiver(post_save, sender=MachineType)
def machine_type_save(sender, instance, created, **kwargs):
    instance.save()
    # if not instance.slug:
    #     slug = slugify(instance.name)
    #     instance.save()
