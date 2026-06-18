from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(verbose_name='Bio', max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True,)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField('Avatar', upload_to='users/profile_avatar/', blank=True, null=True)

    def __str__(self):
        return f'{self.id}_{self.username}'
    
class Followers(models.Model):
    owner = None
    follow_by = None
    pass