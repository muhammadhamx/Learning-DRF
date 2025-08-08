from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author, Post
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender = Author)
def author_created_or_updated(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New Author created: {instance.email}")
        print(f"[SIGNAL] New Author created: {instance.email}")

        Post.objects.create(
            author = instance,
            title = "Welcome Post",
            content = "First post created Automatically"
        )
    else:
        logger.info(f"Author Updated: {instance.email}")
        print(f"[SIGNAL] Author Updated: {instance.email}")