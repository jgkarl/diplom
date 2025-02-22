from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from import_export import resources
from core.models.abstract import AuditableAdmin
from book.models import Book, BookPerson
from person.models import Person
from classifier.models import Item

class BookPersonResource(resources.ModelResource):
    class Meta:
        model = BookPerson
        # fields = ('book_id', 'person_id', 'relation')
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        person_input = row.get('person_id')
        if person_input:
            person_instance = Person.objects.filter(id=person_input).first()
            if person_instance:
                row['person'] = person_instance.id
        type_input = row.get('relation')
        if type_input:
            type_instance = Item.objects.filter(code=type_input, type__identifier='book_person_relation').first()
            if type_instance:
                row['relation'] = type_instance.id

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