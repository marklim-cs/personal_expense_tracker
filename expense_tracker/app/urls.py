from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.handle_signup, name="signup"),
    path("home", views.home, name='home'),
    path("login", views.handle_login, name="login"),
    path("logout", views.handle_logout, name="logout"),
    path("add_expenses", views.add_expenses, name="add_expenses"),
    path("history", views.history, name="history"),
    path("delete_expense", views.delete_expense, name="delete_expense")
]