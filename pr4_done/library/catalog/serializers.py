from rest_framework import serializers
from .models import Book, Author, Genre, Library


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'address']


class BookSerializer(serializers.ModelSerializer):
    library = LibrarySerializer(read_only=True)
    library_id = serializers.PrimaryKeyRelatedField(queryset=Library.objects.all(), source='library', write_only=True)

    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, write_only=True, source='authors')

    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, write_only=True, source='genres')

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_date', 'isbn', 'price', 'rating', 'image',
                  'library', 'library_id',
                  'authors', 'author_ids',
                  'genres', 'genre_ids']

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        genres = validated_data.pop('genres', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        book.genres.set(genres)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        genres = validated_data.pop('genres', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if authors is not None:
            instance.authors.set(authors)
        if genres is not None:
            instance.genres.set(genres)

        return instance
