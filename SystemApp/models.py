from django.db import models
from django.utils import timezone


class Individual(models.Model):
    auth_id = models.IntegerField()


class Vendor(models.Model):
    store_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.store_name


class Transaction(models.Model):
    user = models.ForeignKey(Individual, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    amount = models.FloatField()
    location = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def is_expense(self):
        if self.amount < 0:
            return True

    def __str__(self):
        return self.name + ' ' + str(self.date) + ' ' + str(self.amount)
