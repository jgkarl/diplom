from django.contrib import admin
from classifier.models import Item
from core.models.abstract import AuditableAdmin
from django.urls import reverse
from django.utils.html import format_html
from book.models.resources.BookDepartmentResource import BookDepartmentResource
from django.utils.translation import gettext_lazy as _

class DepartmentFilterSearchForm(admin.SimpleListFilter):
    title = _('Departments')
    parameter_name = 'department'
    template = 'admin/department_search_filter.html'

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

# @admin.register(BookDepartment)
class BookDepartmentAdmin(AuditableAdmin):
    list_display_links = ['type']
    list_display = ['type', 'book_view', 'active']
    resource_class = BookDepartmentResource

    def book_view(self, obj):
        url = reverse("admin:book_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.get_label())