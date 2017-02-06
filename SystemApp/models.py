from django.db import models
from django.utils import timezone


class Individual(models.Model):
    auth_id = models.IntegerField()

    def __str__(self):
        return 'Individual-{0}'.format(self.auth_id)


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


class Features(models.Model):
    user = models.ForeignKey(Individual, on_delete=models.CASCADE)
    student = models.BooleanField(default=False)
    has_kids = models.BooleanField(default=False)
    student_loan = models.IntegerField(default=0)
    pets = models.BooleanField(default=False)
    an_artist = models.BooleanField(default=False)
    proposing = models.BooleanField(default=False)
    athletic = models.BooleanField(default=False)
    divorced = models.BooleanField(default=False)
    outgoing = models.BooleanField(default=False)
    figurine_stuffs = models.BooleanField(default=False)
    peaceful = models.BooleanField(default=False)
    moved = models.BooleanField(default=False)
    into_music = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user',)

