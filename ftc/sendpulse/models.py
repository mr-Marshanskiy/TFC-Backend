from django.db import models

from common.mixins.system import DateMixin


class Template(models.Model):
    id = models.PositiveIntegerField('ID шаблона', primary_key=True)
    name = models.CharField('Название', max_length=255)
    theme = models.CharField('Тема', max_length=255, blank=True, null=True)
    slug = models.CharField('Slug', max_length=255)

    class Meta:
        verbose_name = 'Шаблон письма'
        verbose_name_plural = 'Шаблоны писем'


class Logging(DateMixin):
    response_guid = models.CharField('ID письма', max_length=127,
                                     null=True, blank=True)

    status = models.BooleanField('Успешно отправлено', default=False,
                                 null=True, blank=True)

    template = models.PositiveIntegerField('Шаблон', null=True, blank=True)

    subject = models.CharField('Тема письма', max_length=255,
                               null=True, blank=True)

    sender = models.CharField('Отправитель', max_length=255,
                              null=True, blank=True)

    recipient = models.CharField('Получатель', max_length=255,
                                 null=True, blank=True)

    result = models.JSONField('Ответ JSON', null=True)

    class Meta:
        verbose_name = 'Логи SendPulse'
        verbose_name_plural = 'Логи SendPulse'
