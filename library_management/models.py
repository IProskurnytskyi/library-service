from django.db import models

from library_service import settings


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4, choices=CoverChoices.choices, null=True, blank=True
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=8, decimal_places=2
    )

    def __str__(self) -> str:
        return self.title


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowing"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowing"
    )

    def __str__(self) -> str:
        return f"{self.book.title} ({self.borrow_date})"


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(max_length=7, choices=StatusChoices.choices)
    type = models.CharField(max_length=7, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payment"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(
        max_digits=8, decimal_places=2
    )

    def __str__(self) -> str:
        return f"{self.borrowing} ({self.status})"
