from django.db import models

class PermanentMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    amountInvested = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountPaidThisYear = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profilePic = models.TextField(null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TemporaryMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    amountInvested = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountPaidThisYear = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profilePic = models.TextField(null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class JuniorMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    amountInvested = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountPaidThisYear = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profilePic = models.TextField(null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
