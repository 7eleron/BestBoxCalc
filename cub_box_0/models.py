from django.db import models


# Create your models here.
class calc_count(models.Model):
    reject = models.IntegerField(null=True)
    cut = models.IntegerField(null=True)
    not_production = models.IntegerField(null=True)
    margin = models.IntegerField(null=True)
    manager_proc = models.IntegerField(null=True)
    style_work = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.style_work

    class Meta:
        verbose_name = 'Калькуляция'
        verbose_name_plural = 'Калькуляции'


class Work(models.Model):
    Name = models.TextField(null=True)
    Format = models.CharField(max_length=200, null=True)
    Size = models.CharField(max_length=200, null=True)
    dm2 = models.IntegerField(null=True)
    Tray = models.IntegerField(null=True)
    Lid = models.IntegerField(null=True)
    Content = models.IntegerField(null=True)
    Close_fitting = models.IntegerField(null=True)
    Scotch = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.Name}/{self.Format}'

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'


class Material(models.Model):
    mt_type = models.CharField(max_length=200, null=True)
    mt_name = models.CharField(max_length=200, null=True)
    size_x = models.IntegerField(null=True)
    size_y = models.IntegerField(null=True)
    prise = models.IntegerField(null=True)
    currency = models.CharField(max_length=200, null=True)
    len = models.IntegerField(null=True)

    def __str__(self):
        return self.mt_name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
