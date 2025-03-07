from rest_framework import generics
from api.models import Book
from api.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.filter(id__lt=100)
    serializer_class = BookSerializer

class BookCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        count = Book.objects.count()
        return Response({'count': count})