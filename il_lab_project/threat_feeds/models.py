from django.db import models
import json

class CachedAPIData(models.Model):
    api_name = models.CharField(max_length=50, unique=True)
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.api_name} (Updated: {self.last_updated})"
