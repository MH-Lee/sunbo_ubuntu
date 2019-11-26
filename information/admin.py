from django.contrib import admin
from .models import (Dart, 
                     Rescue,
                     DartUpdateCheck,
                     RescueUpdateCheck)

# Register your models here.
class DartAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name', 'contents_cat')


class RescueAdmin(admin.ModelAdmin):
    list_display = ('date', 'area', 'company_name', 'case_num', 'subject')


class DartUpdateCheckAdmin(admin.ModelAdmin):
    list_display = ('recent_date',)


class RescueUpdateCheckAdmin(admin.ModelAdmin):
    list_display = ('recent_date',)

admin.site.register(Dart, DartAdmin)
admin.site.register(Rescue, RescueAdmin)
admin.site.register(DartUpdateCheck, DartUpdateCheckAdmin)
admin.site.register(RescueUpdateCheck, RescueUpdateCheckAdmin)