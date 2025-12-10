from django.db import models


class Expenditure(models.Model):
    year = models.CharField(max_length=4)
    purpose = models.TextField()
    amountSpent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']  # Most recent first
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'

    def __str__(self):
        return f"{self.year} - {self.purpose[:50]} - ₹{self.amountSpent}"
