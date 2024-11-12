from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.handle_signup, name="signup"),
    path("home", TemplateView.as_view(template_name='home.html'), name='home'),
    path("login", views.handle_login, name="login"),
    path("logout", views.handle_logout, name="logout"),
]