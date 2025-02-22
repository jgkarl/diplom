from django.contrib import admin
from import_export import resources
from core.helpers import get_superuser
from core.models.abstract import AuditableAdmin
from book.models import Book
from classifier.models import Item

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    def before_import_row(self, row, **kwargs):
        format_input = row.get('status')
        if format_input:
            format_instance = Item.objects.filter(code=format_input, type__identifier='book_format').first()
            if format_instance:
                row['format'] = format_instance.id
                
        status_input = row.get('status')
        if status_input:
            status_instance = Item.objects.filter(code=status_input, type__identifier='book_status').first()
            if status_instance:
                row['status'] = status_instance.id
            
    def before_save_instance(self, instance, row, **kwargs):
        superuser = get_superuser()
        instance.created_by = superuser if superuser else None

@admin.register(Book)
class BookAdmin(AuditableAdmin):
    list_editable = ['active']
    list_filter = ['active']
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