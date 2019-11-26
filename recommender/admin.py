from django.contrib import admin
from .models import Recommender

# Register your models here.
class RcommenderAdmin(admin.ModelAdmin):
    list_display = ('company', 'big_predict1')


admin.site.register(Recommender, RcommenderAdmin)