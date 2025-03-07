from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# admin models are registered within the adminModels 
from book.models.admin import BookAdmin, BookCategoryAdmin, BookDepartmentAdmin, BookExtraAdmin, BookLanguageAdmin, BookNameAdmin, BookPersonAdmin, BookResumeAdmin

admin.site.site_header = _('Diplomas')
admin.site.site_title = _('Diplomas')
admin.site.index_title = _('Admin Panel')
