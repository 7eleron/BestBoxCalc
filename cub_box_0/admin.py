from django.contrib import admin
from .models import Work, calc_count, Material


# Register your models here.
admin.site.register(Work)
admin.site.register(calc_count)
admin.site.register(Material)
