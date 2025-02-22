from django.db import models
from core.models.abstract import AuditableModel
from book.models import Book

class BookDepartment(AuditableModel):
    book = models.ForeignKey(Book, related_name='book_departments', on_delete=models.CASCADE)
    type = models.ForeignKey('classifier.Item', related_name='book_department_types', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'book_department_type'} )

    class Meta:
        verbose_name = '[Book Department]'
        verbose_name_plural = '[Book Departments]'
      
    def __str__(self):
        return self.type.name