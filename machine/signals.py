from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Machine, PrintLog


@receiver(post_delete, sender=Machine)
def if_removed_clear_cache(sender, instance, **kwargs):
    # cache.clear()
    cache.delete("machine_machine_count_cache")
    # print(cache.delete("machine_count_cache")) # Returns True if keys cached before


@receiver(post_save, sender=Machine)
def if_crated_clear_cache(sender, instance, created, **kwargs):
    if created:
        # cache.clear() # sadece makine ile ilgili olanları değil her keyi siler. Cache temizleniyor sessiondan atiyor
        cache.delete("machine_machine_count_cache")
        # cache.delete_many(['a', 'b', 'c'])


@receiver(post_delete, sender=PrintLog)
def if_log_removed_clear_cache(sender, instance, **kwargs):
    cache.delete("machine_printlog_count_cache")


@receiver(post_save, sender=PrintLog)
def if_log_crated_clear_cache(sender, instance, created, **kwargs):
    if created:
        print("machine_printlog_count_cache")
        cache.delete("machine_printlog_count_cache")
