from django.contrib import admin
from import_export import resources
from book.models.helpers import get_superuser
from book.models.abstract import AuditableAdmin
from book.models import Book

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    def before_save_instance(self, instance, row, **kwargs):
        superuser = get_superuser()
        instance.created_by = superuser if superuser else None

class BookAdmin(AuditableAdmin):
    list_editable = ['active']
    # list_filter = ['active']
    list_display = ['token', 'published', 'active']
    search_fields = ['token', 'published']
    
    def book_name(self, obj):
        return obj.get_label()

    resource_class = BookResource   
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"An error occurred: {e}", level='error')