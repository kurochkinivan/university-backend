from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Author, Genre, Library
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, LibrarySerializer, AuthorDetailSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('library').prefetch_related('authors', 'genres').order_by('id')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'library': ['exact'],
        'genres': ['exact'],
    }
    search_fields = ['title', 'authors__name']
    ordering_fields = ['title', 'publication_date', 'isbn']

    def get_permissions(self):
        """
        Применяем права доступа только для метода destroy
        """
        if self.action == 'destroy':
            return [IsAuthenticated()]
        return []

    @action(detail=False, url_path='top')
    def top_books(self, request):
        top = self.queryset.order_by('-rating')[:10]
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Удалить книгу",
        description="Удаление книги. Требует авторизацию токеном.",
        responses={
            204: None,
            401: {"description": "Не авторизован"},
            403: {"description": "Нет прав для удаления книги из чужой библиотеки"},
            404: {"description": "Книга не найдена"}
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_libraries = request.user.libraries.all()
        if instance.library not in user_libraries:
            raise PermissionDenied("Вы не можете удалить книгу из чужой библиотеки")
        return super().destroy(request, *args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.request.query_params.get('include') == 'books':
            return AuthorDetailSerializer
        return AuthorSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='include', description='Include related data, e.g., books', required=False, type=str)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='top-books')
    def top_books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all().order_by('-price')[:5]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
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
    queryset = Library.objects.all().order_by('id')
    serializer_class = LibrarySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, url_path='books')
    def books(self, request, pk=None):
        library = self.get_object()
        books = library.books.all()
        page = self.paginate_queryset(books)
        serializer = BookSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
