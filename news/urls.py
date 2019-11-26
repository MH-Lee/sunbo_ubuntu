from django.urls import path
from . import views

urlpatterns = [
    path('lp_company/', views.LP_company_list, name='lp_company'),
    path('main_company/', views.main_company_list, name='main_company'),
    path('portfolio/', views.portfolio_list, name='portfolio'),
    path('professor/', views.professor_list, name='professor'),
    path('investment_news/', views.investment_news_list, name='investment_news'),
    # manual_update
    path('professor_update/', views.professor_data_send, name='professor-update'),
    path('company_update/', views.news_datasend, name='company-update'),
]