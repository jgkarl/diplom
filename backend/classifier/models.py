from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Type(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    active = models.BooleanField(default=True)
    
    identifier = models.CharField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    active = models.BooleanField(default=True)
    code = models.SmallIntegerField(null=False)
    position = models.SmallIntegerField(null=False)
    type = models.ForeignKey(Type, related_name='classifier_type_items', on_delete=models.CASCADE, null=False)
    
    name = models.CharField(max_length=100, unique=True, null=False)
    name_en = models.CharField(max_length=100)

    # automatic fields filled within django-admin actions
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.ForeignKey(User, related_name='created_classifier_items', on_delete=models.CASCADE, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, related_name='updated_classifier_items', on_delete=models.CASCADE, null=True)
    deleted_at = models.DateTimeField(auto_now=True, null=True)
    deleted_by = models.ForeignKey(User, related_name='deleted_classifier_items', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.apply_new_record_fields()
        super().save(*args, **kwargs)

    def apply_new_record_fields(self):
        last_item = Item.objects.filter(type_id=self.type_id).order_by('code').last()
        if last_item:
            self.code = last_item.code + 1
        else:
            self.code = 1

        last_position = Item.objects.filter(type_id=self.type_id).order_by('position').last()
        if last_position:
            self.position = last_position.position + 1
        else:
            self.position = 1