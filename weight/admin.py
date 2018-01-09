from    django.contrib import admin
from .models import *

class WeightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Weight._meta.fields]
    class Meta:
        model=Weight

admin.site.register(Weight,WeightAdmin)
