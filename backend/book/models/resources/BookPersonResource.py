from import_export import resources
from book.models import Book, BookPerson
from person.models import Person
from classifier.models import Item

class BookPersonResource(resources.ModelResource):
    class Meta:
        model = BookPerson
        fields = ('book_id', 'person_id', 'relation')
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance
                row.pop('book_id')
        person_input = row.get('person_id')
        if person_input:
            person_instance = Person.objects.filter(id=person_input).first()
            if person_instance:
                row['person'] = person_instance
                row.pop('person_id')
        type_input = row.get('relation')
        if type_input:
            type_instance = Item.objects.filter(code=type_input, type__identifier='book_person_relation').first()
            if type_instance:
                row['relation'] = type_instance.id
