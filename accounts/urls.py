from django.urls import path

from .views import register, LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),   
]
