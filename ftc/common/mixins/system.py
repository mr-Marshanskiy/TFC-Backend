from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DateMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='Время создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время изменения',
                                      auto_now=True)

    class Meta:
        abstract = True


class InfoMixin(DateMixin):
    created_by = models.ForeignKey(User, verbose_name='Кем создано',
                                   on_delete=models.SET_NULL,
                                   related_name='created_%(class)s', null=True)
    updated_by = models.ForeignKey(User, verbose_name='Кем обновлено',
                                   on_delete=models.SET_NULL,
                                   related_name='updated_%(class)s', null=True)
    models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from crum import get_current_user
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)
