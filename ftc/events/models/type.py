from django.db import models


class Type(models.Model):
    name = models.CharField('Название', max_length=31)
    slug = models.SlugField('Слаг', max_length=15)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы события'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'
