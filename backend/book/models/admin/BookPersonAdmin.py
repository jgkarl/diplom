from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from core.models.abstract import AuditableAdmin
from book.models import BookPerson
from book.models.resources.BookPersonResource import BookPersonResource

@admin.register(BookPerson)
class BookPersonAdmin(AuditableAdmin):
    list_display = ['relation', 'person_view', 'book_view', 'active']
    list_display_links = ['relation']
    list_filter = ['relation', 'active']
    search_fields = ['book__token', 'person__first_name', 'person__last_name']
    resource_class = BookPersonResource
    
    def relation(self, obj):
        return obj.relation.name

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())
    
    def person_view(self, obj):
        url = reverse("admin:person_person_change", args=[obj.person.id])
        return format_html('<a href="{}">{}</a>', url, obj.person.fullname())