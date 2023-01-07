import uuid

from django.db import models

from common.mixins.system import DateMixin


def get_file_dir(i, f):
    folder = str(i.id).split('-')[0]
    return f'files/{folder}/{i.id}_{f}'


class File(DateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=get_file_dir, max_length=255)
    file_name = models.CharField(
        verbose_name='File_name', max_length=255, blank=True, null=True
    )

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        if self.file_name:
            return str(self.file_name)
        return str(self.id)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        return super(File, self).delete(using, keep_parents)

    def get_absolute_url(self, request=None):
        if request is None:
            print('Empty request')
            return None
        try:
            photo_url = self.file.url
            return request.build_absolute_uri(photo_url)
        except Exception as e:
            print(e)
            return None
