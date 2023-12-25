from django.contrib import admin

from library_management.models import (
    Book,
    Borrowing,
    Payment
)


admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Payment)
