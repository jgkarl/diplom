from django.contrib import admin
from import_export import resources
from classifier.models import Item
from core.helpers import get_superuser
from core.models.abstract import AuditableAdmin
from book.models import Book, BookNameInline, BookResumeInline, BookExtraInline, BookCategory, BookDepartment, BookLanguage, BookPerson
from book.models.form.BookForm import BookForm

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    def before_import_row(self, row, **kwargs):
        format_input = row.get('format')
        if format_input:
            format_instance = Item.objects.filter(code=format_input, type__identifier='book_format').first()
            if format_instance:
                row['format'] = format_instance.code
                
        status_input = row.get('status')
        if status_input:
            status_instance = Item.objects.filter(code=status_input, type__identifier='book_status').first()
            if status_instance:
                row['status'] = status_instance.code
            
    def before_save_instance(self, instance, row, **kwargs):
        superuser = get_superuser()
        instance.created_by = superuser if superuser else None

class DepartmentFilterSearchForm(admin.SimpleListFilter):
    title = 'Departments'
    parameter_name = 'department'
    template = 'admin/item_search_filter.html'

    def lookups(self, request, model_admin):
        # Get a list of items for the dropdown
        departments = [(str(department.code), department.name) for department in Item.objects.filter(type__identifier='book_department')]
        # Add an option for "All" at the beginning
        departments.insert(0, ('', 'All'))
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
    list_filter = ['active', DepartmentFilterSearchForm]
    list_display = ['token', 'published', 'book_name','active', 'book_department']
    list_display_links = ['book_name']
    search_fields = ['token', 'published', 'book_names__name']
    
    def book_name(self, obj):
        return obj.get_label()
    
    def book_department(self, obj):
        return obj.get_department()
        
        
    form = BookForm
    autocomplete_fields = ["format", "status"]
    inlines = [BookNameInline, BookResumeInline, BookExtraInline]

    resource_class = BookResource   
    
    def save_model(self, request, obj, form, change):
        try:
            format = form.cleaned_data.get('format')
            if format:
                obj.format = format
            obj.save()

            categories = form.cleaned_data.get('categories')
            if categories:
                BookCategory.objects.bulk_create([
                    BookCategory(type=category, book=obj) for category in categories
                ])

            departments = form.cleaned_data.get('departments')
            if departments:
                BookDepartment.objects.bulk_create([
                    BookDepartment(type=department, book=obj) for department in departments
                ])

            languages = form.cleaned_data.get('languages')
            if languages:
                BookLanguage.objects.bulk_create([
                    BookLanguage(type=language, book=obj) for language in languages
                ])

            authors = form.cleaned_data.get('authors')
            if authors:
                BookPerson.objects.bulk_create([
                    BookPerson.create_author(book=obj, person=author) for author in authors
                ])

            supervisors = form.cleaned_data.get('supervisors')
            if supervisors:
                BookPerson.objects.bulk_create([
                    BookPerson.create_supervisor(book=obj, person=supervisor) for supervisor in supervisors
                ])

            super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"An error occurred: {e}", level='error')