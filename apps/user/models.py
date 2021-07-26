from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, primary_key=True)
    phone = models.CharField('phone', max_length=10)
    entity = models.CharField('entity', max_length=50)
    ADMIN = 0
    SPECIALIST = 1
    STUDENT = 2
    ROLE_CHOICES = ((ADMIN, 'Administrador'), (SPECIALIST, 'Especialista'), (STUDENT, 'Estudiante'))
    role = models.PositiveSmallIntegerField('role', choices=ROLE_CHOICES, default=STUDENT)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.get_full_name()
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_specialist(self):
        return self.role == self.SPECIALIST
    