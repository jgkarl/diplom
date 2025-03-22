from core.models.abstract import AuditableModelResource
from classifier.models import Item
from book.models import Book, BookCategory

class BookCategoryResource(AuditableModelResource):
    class Meta:
        model = BookCategory
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        category_name = row.get('category')
        if category_name:
            type_instance = Item.objects.filter(name=category_name, type__identifier='book_category').first()
            if type_instance:
                row['type'] = type_instance.id
