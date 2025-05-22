from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Author, Genre, Library
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, LibrarySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('library').prefetch_related('authors', 'genres')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'library': ['exact'],
        'genres': ['exact'],
    }
    search_fields = ['title', 'authors__name']
    ordering_fields = ['title', 'publication_date', 'isbn']

    @action(detail=False, url_path='top')
    def top_books(self, request):
        top = self.queryset.order_by('-rating')[:10]
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, url_path='top-books')
    def top_books(self, request, pk=None):
        author = self.get_object()
        books = author.books.order_by('-price')[:5]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        include_books = request.query_params.get('include') == 'books'
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if include_books:
            books = instance.books.all()
            data['books'] = BookSerializer(books, many=True).data
        return Response(data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    @action(detail=True, url_path='books')
    def books(self, request, pk=None):
        genre = self.get_object()
        books = genre.books.all()
        page = self.paginate_queryset(books)
        serializer = BookSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    @action(detail=True, url_path='books')
    def books(self, request, pk=None):
        library = self.get_object()
        books = library.books.all()
        page = self.paginate_queryset(books)
        serializer = BookSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
