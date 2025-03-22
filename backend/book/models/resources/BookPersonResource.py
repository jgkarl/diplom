from core.models.abstract import AuditableModelResource
from book.models import Book, BookPerson
from person.models import Person
from classifier.models import Item

class BookPersonResource(AuditableModelResource):
    class Meta:
        model = BookPerson
        
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
