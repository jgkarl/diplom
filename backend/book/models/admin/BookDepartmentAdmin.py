from django.contrib import admin
from core.models.abstract import AuditableAdmin
from import_export import resources
from django.urls import reverse
from django.utils.html import format_html
from classifier.models import Item
from book.models import Book, BookDepartment

class BookDepartmentResource(resources.ModelResource):
    class Meta:
        model = BookDepartment
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        type_input = row.get('type_id')
        if type_input:
            type_instance = Item.objects.filter(code=type_input, type__identifier='book_department').first()
            if type_instance:
                row['type'] = type_instance.id

@admin.register(BookDepartment)
class BookDepartmentAdmin(AuditableAdmin):
    list_display_links = ['type']
    list_display = ['type', 'book_view', 'active']
    resource_class = BookDepartmentResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())