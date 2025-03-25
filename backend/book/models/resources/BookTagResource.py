from core.models.abstract import AuditableModelResource
from classifier.models import Item
from book.models import Book, BookTag
from tag.models import Tag
from core.helpers import get_superuser

class BookTagResource(AuditableModelResource):
    class Meta:
        model = BookTag
        
    def before_import_row(self, row, **kwargs):
        book_input = row.get('book_id')
        if book_input:
            book_instance = Book.objects.filter(id=book_input).first()
            if book_instance:
                row['book'] = book_instance.id

        tag_name = row.get('tag_name')
        tag_external_id = row.get('tag_link')
        tag_instance = Tag.objects.filter(external_id=tag_external_id).first()
        if not tag_instance:
            tag_instance = Tag.objects.filter(name=tag_name).first()
            if not tag_instance:
                tag_instance = Tag.objects.create(name=tag_name, external_id=tag_external_id)

        row['tag'] = tag_instance.id