from django.db import models

# Create your models here.
class User(models.Model):
    
    user_name = models.CharField()
    user_id = models.CharField()
    user_pw = models.CharField()

    def __str__(self):
        return self.name