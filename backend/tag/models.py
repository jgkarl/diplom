from django.db import models
from uuid import uuid4

class Tag(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    active = models.BooleanField(default=True)
    external_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=False)
    collection = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name