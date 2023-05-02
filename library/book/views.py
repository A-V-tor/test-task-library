from django.http import Http404

from djoser.views import UserViewSet
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import (
    AllBooksSerializer,
    BooksSerializer,
    CustomUserCreateSerializer,
)


class BookAllAPIView(generics.CreateAPIView, generics.ListAPIView):
    """Отображение списка всех книг и создание новой."""

    queryset = Book.objects.all()
    serializer_class = AllBooksSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if Book.objects.filter(title=request.POST.get('title')).exists():
            raise ValidationError('Книга уже существует')
        else:
            return super().create(request, *args, **kwargs)


class BookDetailView(APIView):
    """Отображение кокретной книги, ее изменение и удаление."""

    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BooksSerializer(book)
        return Response(serializer.data)

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BooksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_object(id)
        if book:
            book.delete()
            book.save()
            return Response(f'Книга  {book} удалена')
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    """Создание нового пользователя."""
    serializer_class = CustomUserCreateSerializer
