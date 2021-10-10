from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=80)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)

class Forget_password(models.Model):
    token = models.CharField(max_length=50)
    current_time = models.DateTimeField()
    updated_at = models.DateTimeField(null = True)
    user_id = models.IntegerField()
