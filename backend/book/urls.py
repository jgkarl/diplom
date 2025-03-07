from django.urls import path
from book.views import BookView

urlpatterns = [
    path('', BookView, name='book-view'),
];