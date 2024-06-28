from django.contrib import admin
from apps.expense_tracker.models import Category, Budget, Expense, Alert


# Register your models here.
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Alert)
