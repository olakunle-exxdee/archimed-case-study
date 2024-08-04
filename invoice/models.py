from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Investment(models.Model):
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="investments"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    date = models.DateField()
    fee_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )

    def __str__(self):
        return (
            f"Investor: {self.investor.name}, Amount: {self.amount}, Date: {self.date}"
        )


class Bill(models.Model):
    BILL_TYPES = (
        ("MEMBERSHIP", "Membership"),
        ("UPFRONT", "Upfront Fees"),
        ("YEARLY", "Yearly Fees"),
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="bills"
    )
    investment = models.ForeignKey(
        Investment,
        on_delete=models.CASCADE,
        related_name="bills",
        null=True,
        blank=True,
    )
    bill_type = models.CharField(max_length=10, choices=BILL_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.investor.name} - {self.bill_type} - {self.amount}"


class CapitalCall(models.Model):
    STATUS_CHOICES = (
        ("VALIDATED", "Validated"),
        ("SENT", "Sent"),
        ("PAID", "Paid"),
        ("OVERDUE", "Overdue"),
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="capital_calls"
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    due_date = models.DateField()
    iban = models.CharField(max_length=34)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="VALIDATED"
    )
    bills = models.ManyToManyField(Bill)

    def __str__(self):
        return f"{self.investor.name} - {self.total_amount} due on {self.due_date}"
