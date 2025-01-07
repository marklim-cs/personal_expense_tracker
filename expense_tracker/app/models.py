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
    ("Savings", "Savings"),
    ("Income", "Income"),
    ("Other", "Other"),
]

ADD_EXPENSE = [
    ("Expense", "Expense"),
    ("Income", "Income"),
    ("Saving", "Saving"),
]

PROFESSION = [
    ("Employee", "Employee"),
    ("Business", "Business"),
    ("Student", "Student"),
    ("Other", "Other")
]

class AddMoneyInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    money_type = models.CharField(max_length=20, choices = ADD_EXPENSE)
    quantity = models.IntegerField()
    date = models.DateField(default=now)
    category = models.CharField(max_length=20, choices=SELECT_CATEGORY, default="Food")

    def __str__(self):
        return f"User: {self.user}, {self.money_type}, {self.quantity}, {self.date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20, choices=PROFESSION)
    savings = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.user}"