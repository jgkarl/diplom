from django.contrib import admin
from classifier.models import Item
from core.models.abstract import AuditableAdmin
from book.models import Book, BookNameInline, BookResumeInline, BookExtraInline, BookCategory, BookDepartment, BookLanguage, BookPerson
from book.models.form.BookForm import BookForm
from book.models.resources.BookResource import BookResource
from django.db.models import F
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class DepartmentFilterSearchForm(admin.SimpleListFilter):
    title = _('Departments')
    parameter_name = 'department'
    template = 'admin/item_search_filter.html'

    def lookups(self, request, model_admin):
        # Get a list of items for the dropdown
        departments = [(str(department.code), department.name) for department in Item.objects.filter(type__identifier='book_department')]
        # Add an option for "All" at the beginning
        departments.insert(0, ('', _('All')))
        return departments

    def queryset(self, request, queryset):
        department_id = self.value()
        if department_id:
            return queryset.filter(book_departments__type__code=department_id)

    def choices(self, changelist):
        super().choices(changelist)
        return (
            *self.lookup_choices,
        )

@admin.register(Book)
class BookAdmin(AuditableAdmin):
    list_editable = ['active']
    list_filter = ['active', DepartmentFilterSearchForm, 'updated_at']
    list_display = ['token', 'published','book_author', 'book_name', 'book_categories', 'book_supervisor', 'book_department', 'status', 'updated_at', 'active']

    list_display_links = ['book_name']
    search_fields = ['token', 'published', 'book_names__name', 'book_persons__person__first_name', 'book_persons__person__last_name']
    ordering = [F("updated_at").desc(nulls_last=True)]

    def book_name(self, obj):
        return obj.get_label()
    
    book_name.short_description = _("Book Title")
    
    def book_department(self, obj):
        return obj.get_department()
    
    book_department.short_description = _("Department")
    
    def book_categories(self, obj):
        categories = obj.book_categories.all()
        return format_html(", ".join([f"<span style='background-color: #e0e0e0; border-radius: 5px; padding: 2px 5px;'>{category.type.name}</span>" for category in categories]))
    
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