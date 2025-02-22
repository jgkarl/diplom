from uuid import uuid4
from django.utils import timezone
from django.db import models
from import_export.admin import ImportExportActionModelAdmin

class AuditableModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='created_%(class)s_set', null=True, blank=True, editable=False, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey('auth.User', related_name='updated_%(class)s_set', null=True, blank=True, on_delete=models.SET_NULL)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('auth.User', related_name='deleted_%(class)s_set', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{'ACTIVE' if self.active else 'INACTIVE'}-v{self.version}-{self.uuid}"
    

class AuditableAdmin(ImportExportActionModelAdmin):
    list_editable = ['active']
    list_filter = ['active']
    exclude = ['version', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by']
    actions = ['activate', 'deactivate', 'delete_selected']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ['active']

    def status(self, obj):
        if obj.deleted_at and obj.deleted_by:
            return f"Deleted at {obj.deleted_at.strftime('%Y-%m-%d %H:%M:%S')} by {obj.deleted_by}"
        if obj.updated_at and obj.updated_by:
            return f"Updated at {obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')} by {obj.updated_by}"
        return f"Created at {obj.created_at.strftime('%Y-%m-%d %H:%M:%S')} by {obj.created_by}"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Object is being created
            obj.created_at = timezone.now()
            obj.created_by = request.user
        obj.updated_at = timezone.now()
        obj.updated_by = request.user
        obj.version += 1
        super().save_model(request, obj, form, change)

    # Soft delete
    def delete_model(self, request, obj):
        obj.deleted_at = timezone.now()
        obj.deleted_by = request.user
        obj.active = False
        obj.save()
    
    # Custom actions for bulk operations
    def deactivate(self, request, queryset):
        queryset.update(active=False)
    
    def activate(self, request, queryset):
        queryset.update(active=True)
    