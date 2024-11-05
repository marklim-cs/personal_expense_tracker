from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

SELECT_CATEGORY = [
    ("Food", "Food"),
    ("Travel", "Travel"),
    ("Shopping", "Shopping"),
    ("Necessities", "Necessities"),
    ("Entertainment", "Entertainment"),
    ("Other", "Other")
]

ADD_EXPENSE = [
    ("Expense", "Expense"),
    ("Income", "Income")
]

PROFESSION = [
    ("Employee", "Employee"),
    ("Business", "Business"),
    ("Student", "Student"),
    ("Other", "Other")
]

class AddMoneyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE),
    add_money = models.CharField(choices = ADD_EXPENSE),
    quantity = models.IntegerField(),
    date = models.DateField(default=now),
    category = models.CharField(choices=SELECT_CATEGORY, default="Food")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE),
    proffesion = models.CharField(max_length=20, choices=PROFESSION),
    savings = models.IntegerField(null=True, blank=True),
    income = models.IntegerField(null=True, blank=True)
    