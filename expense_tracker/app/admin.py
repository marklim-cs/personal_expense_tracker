from django.contrib import admin
from .models import AddMoneyInfo, UserProfile

# Register your models here.
class AddMoneyInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "date", "category", "add_money")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profession", "savings", "income")

admin.site.register(AddMoneyInfo, AddMoneyInfoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)