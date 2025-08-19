from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    first_name: None
    last_name: None
    
    name = models.CharField()
    is_corporate = models.BooleanField(default=False)
    corporate = models.ForeignKey('partners.Company', on_delete=models.CASCADE, related_name='members', blank=True)

    def __str__(self):
        return self.name