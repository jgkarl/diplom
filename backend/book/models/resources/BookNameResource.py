from import_export import resources
from classifier.models import Item
from book.models import Book, BookName

class BookNameResource(resources.ModelResource):
    class Meta:
        model = BookName
        exclude = ('uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
        
    def before_import_row(self, row, **kwargs):       
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id
        type_input = row.get('type_id')
        if type_input:
            type_instance = Item.objects.filter(code=type_input, type__identifier='book_name_type').first()
            if type_instance:
                row['type'] = type_instance.id
