from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('wallet/', views.wallet, name='wallet'),
]