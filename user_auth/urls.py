from django.urls import path
from . import views

urlpatterns = [
    path('', views.key_auth_page, name='key_auth_page'),
]
