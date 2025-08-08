from django.db import models
from django.utils import timezone
from datetime import timedelta

class AuthorManager(models.Manager):
    def by_role(self, role):
        # Return author filterted by given role
        return self.get_queryset().filter(role=role)
    
    def recent(self, days=7):
        # Return authors created in the last `days` days.
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(created_at__gte = cutoff_date )
    def search_name(self, keyword):
        # Return authors whose name contain keywords (it's a case sensitive)
        return self.get_queryset().filter(__name__icontains = keyword)  