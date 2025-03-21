from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from core.models.abstract import AuditableAdmin
from book.models import BookResume
from book.models.resources.BookResumeResource import BookResumeResource

@admin.register(BookResume)
class BookResumeAdmin(AuditableAdmin):
    list_display = ['has_resume', 'language', 'name', 'book_view', 'active']
    resource_class = BookResumeResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())
