from django.db import models
#from django.contrib.auth.models import AbstractUser
class user(models.Model):
    username=models.CharField(max_length=16)
    password=models.CharField(max_length=32)
    cor=models.CharField(max_length=100,default='')
    dep=models.CharField(max_length=100,default='')

class doc(models.Model):
    docname=models.CharField(max_length=30)
    content=models.TextField(max_length=1000)
    createdtime=models.TextField(max_length=32)
    file=models.CharField(max_length=100)
    author=models.ForeignKey(user,on_delete=models.CASCADE)


# Create your models here.
