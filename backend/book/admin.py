from django.contrib import admin
from book.models import Book
from book.models.admin.BookAdmin import BookAdmin

admin.site.site_header = 'Diplomitööde Admin'
admin.site.site_title = 'Diplom Admin'
admin.site.index_title = 'Admin Panel'

admin.site.register(Book, BookAdmin)