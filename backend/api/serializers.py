# serializers.py
from rest_framework import serializers
from api.models import Book
from person.models import Person

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'uuid', 'active', 'token')
        
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('uuid', 'first_name', 'last_name')

class Select2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'fullname')