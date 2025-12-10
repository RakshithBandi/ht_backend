from django.db import models

class ChitFund(models.Model):
    year = models.IntegerField()
    permanentAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    temporaryAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    juniorAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    villageContribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    otherContributions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inputGrandTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grandTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amountSpent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)
