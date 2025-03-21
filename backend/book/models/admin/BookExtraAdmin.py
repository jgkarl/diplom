from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from core.models.abstract import AuditableAdmin
from book.models import BookExtra
from book.models.resources.BookExtraResource import BookExtraResource

@admin.register(BookExtra)
class BookExtraAdmin(AuditableAdmin):
    list_display_links = ['name']
    list_display = ['name', 'type', 'book_view', 'active']
    resource_class = BookExtraResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())