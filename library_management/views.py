from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from library_management.models import (
    Book,
    Borrowing
)
from library_management.permissions import IsAdminOrReadOnly
from library_management.serializers import (
    BookSerializer,
    BorrowingSerializer,
    BorrowingManageSerializer,
    BorrowingRetrieveSerializer,
    BorrowingReturnSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Type:
        if self.action in ("create", "update", "partial_update"):
            return BorrowingManageSerializer

        if self.action == "retrieve":
            return BorrowingRetrieveSerializer

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return BorrowingSerializer

    def create(self, request, *args, **kwargs) -> Response:
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)

        if book.inventory > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            book.inventory -= 1
            book.save()

            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {"message": "Book not available for borrowing"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        user_id = ""
        if self.request.user.is_staff is True:
            user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        queryset = self.queryset

        if self.request.user.is_staff is False:
            queryset = queryset.filter(user_id=self.request.user.id)

        if user_id:
            queryset = queryset.filter(user_id=int(user_id))

        if is_active:
            if is_active == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    @action(methods=["PUT"], detail=True, url_path="return")
    def return_borrowing(self, request, pk=None) -> Response:
        """Endpoint for returning a book"""
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)

        if borrowing.actual_return_date is None:
            serializer.save()
            borrowing.book.inventory += 1
            borrowing.book.save()

            return Response(
                {"message": "Book returned successfully"},
                status=status.HTTP_200_OK
            )

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
