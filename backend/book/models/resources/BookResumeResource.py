from import_export import resources
from book.models import Book, BookResume
from classifier.models import Item

class BookResumeResource(resources.ModelResource):
    class Meta:
        model = BookResume
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
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
