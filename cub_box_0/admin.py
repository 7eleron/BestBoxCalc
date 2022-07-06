from django.contrib import admin
from .models import Work, calc_count, Material, Work2


# Register your models here.
class WorkAdm(admin.ModelAdmin):
    list_display = ('Name', 'Format', 'dm2', 'Tray', 'Lid', 'Close_fitting', 'Scotch')


class WorkAdm2(admin.ModelAdmin):
    list_display = ('Size', 'Hight', 'Count')


class CalcAdm(admin.ModelAdmin):
    list_display = ('reject', 'cut', 'not_production', 'margin', 'manager_proc', 'style_work')


class MatAdm2(admin.ModelAdmin):
    list_display = ('mt_type', 'mt_name', 'size_x', 'size_y', 'prise', 'currency')


admin.site.register(Work, WorkAdm)
admin.site.register(Work2, WorkAdm2)
admin.site.register(calc_count, CalcAdm)
admin.site.register(Material, MatAdm2)

