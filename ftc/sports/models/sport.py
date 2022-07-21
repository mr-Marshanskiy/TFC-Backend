from django.db import models


class Sport(models.Model):
    name = models.CharField('Название', max_length=63)
    slug = models.SlugField('Слаг', max_length=31)
    description = models.TextField('Описание', null=True, blank=True)
    icon = models.TextField('Изображение', null=True, blank=True)

    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'
