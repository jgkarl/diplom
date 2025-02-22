from django.contrib import admin

# admin models are registered within the adminModels 
from book.models.admin import BookAdmin, BookCategoryAdmin, BookDepartmentAdmin, BookExtraAdmin, BookLanguageAdmin, BookNameAdmin, BookPersonAdmin, BookResumeAdmin
from book.models import BookRelatedBook

admin.site.site_header = 'Diplomitööde Admin'
admin.site.site_title = 'Diplom Admin'
admin.site.index_title = 'Admin Panel'
