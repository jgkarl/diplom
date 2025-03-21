from django.contrib import admin
from core.models.abstract import AuditableAdmin
from django.urls import reverse
from django.utils.html import format_html
from book.models import BookDepartment
from book.models.resources.BookDepartmentResource import BookDepartmentResource

@admin.register(BookDepartment)
class BookDepartmentAdmin(AuditableAdmin):
    list_display_links = ['type']
    list_display = ['type', 'book_view', 'active']
    resource_class = BookDepartmentResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())