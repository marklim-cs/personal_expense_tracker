from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('signup', views.handle_signup, name="signup"),
    path('registered', TemplateView.as_view(template_name='registered.html'), name='registered')
]