from django.contrib import admin
from core.models.abstract import AuditableAdmin
from django.urls import reverse
from django.utils.html import format_html
from book.models import BookCategory
from book.models.resources.BookCategoryResource import BookCategoryResource

@admin.register(BookCategory)
class BookCategoryAdmin(AuditableAdmin):
    list_display_links = ['type']
    list_display = ['type', 'book_view', 'active']
    resource_class = BookCategoryResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())