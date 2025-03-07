from django.urls import path
from book.views import home, list, details

urlpatterns = [
    path("", home, name="bookHome"),
    path("list", list, name="bookList"),
    # book views
    path("<int:pk>", details, name="bookDetails"),
    path("<int:pk>/details", details, name="bookDetails"),
]
