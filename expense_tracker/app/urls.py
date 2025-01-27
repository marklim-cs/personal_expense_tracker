from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("home", views.home, name='home'),
    path("login", views.log_in, name="login"),
    path("logout", views.logout, name="logout"),
    path("add_expenses", views.add_expenses, name="add_expenses"),
    path("history", views.history, name="history"),
    path("delete_expense", views.delete_expense, name="delete_expense"),
    path("thirty_days", views.thirty_days_summary, name="thirty_days"),
    path("one_week", views.one_week_summary, name="one_week"),
    path("year_to_date", views.year_to_date_summary, name="year_to_date"),
    path("update_profile", views.update_profile, name="update_profile"),
]