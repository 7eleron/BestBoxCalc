from django.db import models


# Create your models here.
class calc_count(models.Model):
    reject = models.FloatField(null=True)
    cut = models.IntegerField(null=True)
    not_production = models.FloatField(null=True)
    margin = models.FloatField(null=True)
    manager_proc = models.FloatField(null=True)
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
    dm2 = models.FloatField(null=True)
    Tray = models.FloatField(null=True)
    Lid = models.FloatField(null=True)
    Content = models.FloatField(null=True)
    Close_fitting = models.IntegerField(null=True)
    Scotch = models.FloatField(null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Работа автомат'
        verbose_name_plural = 'Работы автомат'


class Material(models.Model):
    mt_type = models.CharField(max_length=200, null=True)
    mt_name = models.CharField(max_length=200, null=True)
    size_x = models.IntegerField(null=True)
    size_y = models.IntegerField(null=True)
    prise = models.FloatField(null=True)
    currency = models.CharField(max_length=200, null=True)
    len = models.FloatField(null=True)

    def __str__(self):
        return self.mt_name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Work2(models.Model):
    Size = models.IntegerField(null=True)
    Hight = models.IntegerField(null=True)
    Count = models.FloatField(null=True)

    def __str__(self):
        return self.Size

    class Meta:
        verbose_name = 'Работа ручная'
        verbose_name_plural = 'Работы ручная'


class Kroy(models.Model):
    name = models.CharField(max_length=50)
    kroy_Img = models.ImageField(upload_to='images_kroy/')


class PressFoil(models.Model):
    quantity = models.IntegerField(default=0)
    preparation = models.IntegerField(default=0)
    push = models.IntegerField(default=0)


class Printing(models.Model):
    quantity = models.IntegerField(default=0)
    preparation = models.IntegerField(default=0)
    push = models.IntegerField(default=0)

