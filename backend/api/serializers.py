# serializers.py
from rest_framework import serializers
from api.models import Book
from person.models import Person
from tag.models import Tag

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'uuid', 'active', 'token', 'published')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['title'] = instance.get_label() # Map 'get_label' to 'title'
        representation['authors'] = [
            Person.objects.get(id=author_id).fullname() for author_id in instance.get_authors()
        ]
        return representation

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('uuid', 'first_name', 'last_name')

class PersonS2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id',)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['text'] = instance.fullname()
        return representation

class TagS2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['text'] = instance.name
        return representation