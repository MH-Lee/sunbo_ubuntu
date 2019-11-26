from django.urls import path, include
from . import views
from .api.views import DartAPIView, RescueAPIView

urlpatterns = [
    path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('dart_list/', views.dart_list, name='dart_list'),
    path('rescue_detail/<int:pk>/', views.rescue_detail, name='rescue_detail'),
    path('api/rescue/', RescueAPIView.as_view(), name='rescue_api'),
    path('api/dart/', DartAPIView.as_view(), name='dart_api'),
    # manual update
    path('dart_update/', views.dart_data_send, name='dart_update'),
    path('rescue_update/', views.rescue_data_send, name='rescue_update'),
]
