from core.models.abstract import AuditableModelResource
from classifier.models import Item
from book.models import Book

class BookResource(AuditableModelResource):
    class Meta:
        model = Book

    def before_import_row(self, row, **kwargs):
        format_input = row.get('format')
        if format_input:
            format_instance = Item.objects.filter(code=format_input, type__identifier='book_format').first()
            if format_instance:
                row['format'] = format_instance.id

        status_input = row.get('status')
        if status_input:
            status_instance = Item.objects.filter(code=status_input, type__identifier='book_status').first()
            if status_instance:
                row['status'] = status_instance.id