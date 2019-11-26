from django.urls import path, include
from . import views

urlpatterns = [
    path('deal_list/', views.dfb_list, name='dfb_list'),
    path('update/', views.manual_update, name='dfb_update')
]
