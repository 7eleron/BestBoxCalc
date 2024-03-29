from django.contrib import admin
from .models import Work, calc_count, Material, Work2, Kroy, PressFoil, Printing


# Register your models here.
class WorkAdm(admin.ModelAdmin):
    list_display = ('Name', 'Format', 'dm2', 'Tray', 'Lid', 'Close_fitting', 'Scotch')
    search_fields = ('Name', 'dm2', 'Tray', 'Lid')
    fields = ('dm2', 'Tray', 'Lid')
    list_editable = ('dm2', 'Tray', 'Lid')


class WorkAdm2(admin.ModelAdmin):
    list_display = ('Size', 'Hight', 'Count')
    search_fields = ('Size', 'Hight', 'Count')
    fields = ('Count',)
    list_editable = ('Count',)


class CalcAdm(admin.ModelAdmin):
    list_display = ('reject', 'cut', 'not_production', 'margin', 'manager_proc', 'style_work')
    search_fields = ('reject', 'cut', 'not_production', 'margin', 'manager_proc', 'style_work')
    fields = ('reject', 'cut', 'not_production', 'margin', 'manager_proc')
    list_editable = ('cut', 'not_production', 'margin', 'manager_proc')


class MatAdm2(admin.ModelAdmin):
    list_display = ('mt_type', 'mt_name', 'size_x', 'size_y', 'prise', 'currency')
    search_fields = ('mt_type', 'mt_name', 'size_x', 'size_y', 'prise', 'currency')
    fields = ('mt_type', 'mt_name', 'size_x', 'size_y', 'prise', 'currency')
    list_editable = ('prise',)


class KroyAdm(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PressFoilAdm(admin.ModelAdmin):
    list_display = ('quantity', 'preparation', 'push',)
    search_fields = ('quantity',)


class PrintingAdm(admin.ModelAdmin):
    list_display = ('quantity', 'preparation', 'push',)
    search_fields = ('quantity',)


admin.site.register(Work, WorkAdm)
admin.site.register(Work2, WorkAdm2)
admin.site.register(calc_count, CalcAdm)
admin.site.register(Material, MatAdm2)
admin.site.register(Kroy, KroyAdm)
admin.site.register(PressFoil, PressFoilAdm)
admin.site.register(Printing, PrintingAdm)

