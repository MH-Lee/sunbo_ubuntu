from django.contrib import admin
from .models import (InvestNews,
                    LPCompany,
                    MainCompany,
                    Portfolio,
                    Professor,
                    NewsUpdateCheck,
                    ProfessorUpdateCheck,)

# Register your models here.
class InvestNewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'news_title', 'news_url')


class LPCompanyAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name', 'news_title')


class MainCompanyAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name', 'news_title')


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('date', 'news_title', 'small_class_1')


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name', 'news_title')


class NewsUpdateCheckAdmin(admin.ModelAdmin):
    list_display = ('recent_date',)


class ProfessorUpdateCheckAdmin(admin.ModelAdmin):
    list_display = ('recent_date',)


admin.site.register(InvestNews, InvestNewsAdmin)
admin.site.register(LPCompany, LPCompanyAdmin)
admin.site.register(MainCompany, MainCompanyAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(NewsUpdateCheck, NewsUpdateCheckAdmin)
admin.site.register(ProfessorUpdateCheck, ProfessorUpdateCheckAdmin)