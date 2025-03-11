from django.contrib import admin
from core.models.abstract import AuditableAdmin
from import_export import resources
from django.urls import reverse
from django.utils.html import format_html
from classifier.models import Item
from book.models import Book, BookCategory

class BookCategoryResource(resources.ModelResource):
    class Meta:
        model = BookCategory
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        category_name = row.get('category')
        if category_name:
            type_instance = Item.objects.filter(name=category_name, type__identifier='book_category').first()
            if type_instance:
                row['type'] = type_instance.id

@admin.register(BookCategory)
class BookCategoryAdmin(AuditableAdmin):
    list_display_links = ['type']
    list_display = ['type', 'book_view', 'active']
    resource_class = BookCategoryResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())