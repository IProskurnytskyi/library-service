from rest_framework import viewsets

from library_management.models import Book
from library_management.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
