from import_export import resources
from book.models import Book, BookExtra
from classifier.models import Item

class BookExtraResource(resources.ModelResource):
    class Meta:
        model = BookExtra
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
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
