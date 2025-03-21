from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from core.models.abstract import AuditableAdmin
from book.models import BookName
from book.models.resources.BookNameResource import BookNameResource

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
