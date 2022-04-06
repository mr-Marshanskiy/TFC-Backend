import uuid
from django.db import models

from common.tools.file import get_file_dir


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=get_file_dir, max_length=255)
    file_name = models.CharField(verbose_name='Название файла', max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='Когда создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Когда обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Файлы'
        verbose_name_plural = 'Файл'

    def __str__(self):
        if self.file_name:
            return str(self.file_name)
        return str(self.id)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        return super(File, self).delete(using, keep_parents)
