from django.db import models
from core.models.abstract import AuditableModel
from book.models import Book
from person.models import Person
from classifier.models import Item

class BookPerson(AuditableModel):
    book = models.ForeignKey(Book, related_name='book_persons', on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, related_name='person_related_books', on_delete=models.DO_NOTHING)
    relation = models.ForeignKey('classifier.Item', related_name='book_person_relations', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'book_person_relation'} ) 
    
    def __str__(self):
        return self.relation.name + ': ' + self.person.fullname()
    
    def create_author(book, person):
        return BookPerson(relation=Item.objects.get(name_en='author'), book=book, person=person)
    
    def create_supervisor(book, person):
        return BookPerson(relation=Item.objects.get(name_en='supervisor'), book=book, person=person)