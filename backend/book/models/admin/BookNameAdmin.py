from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from import_export import resources
from classifier.models import Item
from core.models.abstract import AuditableAdmin
from book.models import Book, BookName

class BookNameResource(resources.ModelResource):
    class Meta:
        model = BookName
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        type_input = row.get('type_id')
        if type_input:
            type_instance = Item.objects.filter(code=type_input, type__identifier='book_name_type').first()
            if type_instance:
                row['type'] = type_instance.id

@admin.register(BookName)
class BookNameAdmin(AuditableAdmin):
    list_display = ['name', 'type', 'book_view', 'active']
    resource_class = BookNameResource
    
    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())
    
    formfield_overrides = {
        models.CharField: {
            "widget": admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})
        },
    }
