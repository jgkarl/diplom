from core.models.abstract import AuditableModelResource
from book.models import Book, BookExtra
from classifier.models import Item

class BookExtraResource(AuditableModelResource):
    class Meta:
        model = BookExtra
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        item_input = row.get('type_id')
        if item_input:
            item_instance = Item.objects.filter(code=item_input, type__identifier='book_extra').first()
            if item_instance:
                row['type'] = item_instance.id
