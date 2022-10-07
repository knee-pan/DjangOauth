from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Machine


@receiver(post_delete, sender=Machine)
def if_removed_clear_cache(sender, instance, **kwargs):
    # cache.clear()
    cache.delete("log_count_cache")
    # print(cache.delete("log_count_cache")) # Returns True if keys cached before


@receiver(post_save, sender=Machine)
def if_crated_clear_cache(sender, instance, created, **kwargs):
    """Cache temizleniyor sessiondan atiyor"""
    if created:
        print("calisti")
        # cache.clear() # sadece makine ile ilgili olanları değil her keyi siler.
        print(cache.delete("machine_count_cache"))
