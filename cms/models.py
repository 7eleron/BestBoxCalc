from django.db import models


# Create your models here.
class CmsSlider(models.Model):
    cms_img = models.ImageField(upload_to='sliderimg/')
    cms_construction = models.CharField(max_length=200, verbose_name='Конструкция')
    cms_link = models.CharField(max_length=200, null=True, default='-', verbose_name='Ссылка на конструкцию')
    cms_css = models.CharField(max_length=200, null=True, default='-', verbose_name='CSS klass')

    def __str__(self):
        return self.cms_construction

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
