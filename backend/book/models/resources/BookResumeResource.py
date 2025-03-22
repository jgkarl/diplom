from django.utils.timezone import now
from core.models.abstract import AuditableModelResource
from book.models import Book, BookResume
from core.helpers import get_superuser
from classifier.models import Item

class BookResumeResource(AuditableModelResource):
    class Meta:
        model = BookResume
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        item_input = row.get('language_id')
        if item_input:
            item_instance = Item.objects.filter(code=item_input, type__identifier='language').first()
            if item_instance:
                row['language'] = item_instance.id