from rest_framework import generics
from api.models import Book
from api.serializers import BookSerializer, PersonSerializer, PersonS2Serializer, TagS2Serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from person.models import Person
from tag.models import Tag


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.filter(id__lt=100)
    serializer_class = BookSerializer

class BookModelAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BookCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        count = Book.objects.count()
        return Response({"count": count})


class PersonListAPIView(generics.ListAPIView):
    queryset = Person.objects.filter(id__lt=1010)
    serializer_class = PersonSerializer


class PersonSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        if query:
            persons = Person.objects.filter(first_name__icontains=query) | Person.objects.filter(last_name__icontains=query)
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data)
        return Response({"error": "No query provided"}, status=400)

class PersonQueryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        if query:
            persons = Person.objects.filter(first_name__icontains=query) | Person.objects.filter(last_name__icontains=query)
            serializer = PersonS2Serializer(persons, many=True)
            return Response(serializer.data)
        return Response({"error": "No query provided"}, status=400)

class TagQueryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        if query:
            persons = Tag.objects.filter(name__icontains=query)
            serializer = TagS2Serializer(persons, many=True)
            return Response(serializer.data)
        return Response({"error": "No query provided"}, status=400)