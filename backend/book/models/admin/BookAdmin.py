from django.contrib import admin
from book.models.admin.BookDepartmentAdmin import DepartmentFilterSearchForm
from core.models.abstract import AuditableAdmin
from book.models import Book, BookNameInline, BookResumeInline, BookExtraInline
from book.models.form.BookForm import BookForm
from book.models.resources.BookResource import BookResource
from django.db.models import F
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Book)
class BookAdmin(AuditableAdmin):
    list_editable = []
    list_filter = [DepartmentFilterSearchForm, 'updated_at']
    list_display = ['token', 'published','book_author', 'book_name', 'book_categories', 'book_tags', 'book_supervisor', 'updated_at']


    list_display_links = ['book_name']
    search_fields = ['token', 'published', 'book_names__name', 'book_persons__person__first_name', 'book_persons__person__last_name']
    ordering = [F("updated_at").desc(nulls_last=True)]

    def book_name(self, obj):
        return obj.get_label()
    
    book_name.short_description = _("Book Title")
    
    def book_department(self, obj):
        return obj.get_department()
    
    book_department.short_description = _("Department")
    
    def book_tags(self, obj):
        book_tags = obj.book_tags.all()
        return format_html(", ".join([f"{tag.tag.name}" for tag in book_tags]))
    
    book_tags.enable_tags = True
    book_tags.short_description = _("Book Tags")
    
    def book_categories(self, obj):
        categories = obj.book_categories.all()
        return format_html(", ".join([f"{category.type.name}" for category in categories]))
    
    book_categories.enable_tags = True
    book_categories.short_description = _("Categories")
    
    def book_author(self, obj):
        return ", ".join(obj.authors())
    
    book_author.short_description = _("Authors")
    
    def book_supervisor(self, obj):
        return ", ".join(obj.supervisors())
    
    book_supervisor.short_description = _("Supervisors")
    
    form = BookForm
    autocomplete_fields = ["format", "status"]
    inlines = [BookNameInline, BookResumeInline, BookExtraInline]
    resource_class = BookResource