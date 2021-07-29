from django.db import models

# Create your models here.
class Model(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    path = models.FileField(upload_to='uploads/models')
    is_active = models.BooleanField('active', default=True)

    class Meta:
        verbose_name = 'model'
        verbose_name_plural = 'models'
