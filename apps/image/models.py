from django.db import models

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    path = models.FileField(upload_to='uploads/')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
    