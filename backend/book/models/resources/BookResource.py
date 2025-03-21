from import_export import resources
from classifier.models import Item
from core.helpers import get_superuser
from book.models import Book

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
