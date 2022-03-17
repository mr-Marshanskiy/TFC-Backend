from django.db import models


class DictAbstract(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('Слаг', max_length=31)
    description = models.TextField('Описание', null=True, blank=True)
    sort = models.PositiveSmallIntegerField('Сортировка', null=True, blank=True)
    active = models.BooleanField('Активный', default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'
