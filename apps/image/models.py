from django.db import models

# Create your models here.
def get_upload_path(instance, filename):
    return 'uploads/images/{}/{}'.format(instance.type, filename)

class Image(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    path = models.FileField(upload_to=get_upload_path) 
    T1 = 1
    T2 = 2
    TYPE_CHOICES = ((T1, 't1'), (T2, 't2'))
    type = models.PositiveSmallIntegerField('type', choices=TYPE_CHOICES, default=T1)

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
    