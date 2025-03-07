from django.urls import path
from api.views import BookListAPIView, BookCountAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Diplom API",
        default_version='v1',
        description="API documentation for Diploms",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="license"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)

# TODO: allow schema and documentation for public
urlpatterns = [
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# TODO: add api jwt token autorization for query
urlpatterns += [
    path('v1/book', BookListAPIView.as_view(), name='book-api'),
    path('v1/book/count', BookCountAPIView.as_view(), name='book-count-api'),
]
