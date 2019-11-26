from django.contrib import admin
from .models import DealFlowBox
# Register your models here.
class DealFlowBoxAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name')

admin.site.register(DealFlowBox, DealFlowBoxAdmin)
