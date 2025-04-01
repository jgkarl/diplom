from django.urls import path
from book.views import home, list, details, search

urlpatterns = [
    path("", home, name="bookHome"),
    path("list", list, name="bookList"),
    path("search", search, name="bookSearch"),
    # book views
    path("<int:pk>", details, name="bookDetails"),
    path("<int:pk>/details", details, name="bookDetails"),
]
