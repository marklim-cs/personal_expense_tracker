from django.contrib import admin
from .models import AddMoneyInfo, UserProfile

# Register your models here.
class AddMoneyInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "date", "category", "add_money")

admin.site.register(AddMoneyInfo, AddMoneyInfoAdmin)
admin.site.register(UserProfile)