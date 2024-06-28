from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

## Custom 
from apps.core.models import TimestampedModel


from decimal import Decimal



# Create your models here.

"""
    #! Category Model
"""
class Category(TimestampedModel):
    name = models.CharField(
            verbose_name="Budget Category Name",
            max_length=255,
            unique=True
        )

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name", "-created_at"]



"""
    #! Budget Model
"""
class Budget(TimestampedModel):
    owner = models.ForeignKey(
                User, 
                on_delete=models.CASCADE, 
                related_name="budgets", 
                verbose_name="Owner"
            ) 
    
    category = models.ForeignKey(
                Category, 
                on_delete=models.CASCADE, 
                related_name="budgets", 
                verbose_name="Category"
            )

    amount = models.DecimalField(
                verbose_name="Amount",
                default=10,
                decimal_places=2,
                max_digits=10,
                validators=[MinValueValidator(Decimal("0.01"))],
            )

    def __str__(self):
        return f"{self.owner.get_full_name()} - {self.category.name} - {self.amount}"
    
    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ('owner', 'category')
        ordering = ["-created_at"]




"""
    #! Expense Model
"""
class Expense(TimestampedModel):
    owner = models.ForeignKey(
                User, 
                on_delete=models.CASCADE, 
                related_name="expenses", 
                verbose_name="Owner"
            ) 
    
    category = models.ForeignKey(
                Category,
                on_delete=models.CASCADE,
                related_name="expenses",
                verbose_name="Category"
            )

    amount = models.DecimalField(
                verbose_name="Amount",
                blank=False,
                default=10,
                decimal_places=2,
                max_digits=10,
                validators=[MinValueValidator(Decimal("0.01"))]
            )
    
    description = models.TextField(
                verbose_name="Description",
                null=True,
                blank=True
            )

    def __str__(self):
        return f"{self.owner.get_full_name()} - {self.category.name} - {self.amount}"
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Expense amount must be greater than 0.")
        
    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-created_at"]



"""
    #! Alert Model
"""
class Alert(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="alerts",
        verbose_name="User"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="alerts",
        verbose_name="Category"
    )

    message = models.CharField(
        verbose_name="Alert Message",
        max_length=255
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category.name} - {self.message}"

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ["-created_at"]

# You can create custom validators if necessary
def validate_budget_amount(value):
    if value < 0:
        raise ValidationError("Budget amount must be positive.")

def validate_expense_amount(value):
    if value <= 0:
        raise ValidationError("Expense amount must be greater than 0.")