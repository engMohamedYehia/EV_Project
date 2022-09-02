
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100,null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    create = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True)
    group = models.ManyToManyField(Group)


class Report(models.Model):
    title = models.CharField(max_length=100,null=True)
    tage = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    create = models.DateField(auto_now_add=True, null=True)
    upload_file = models.FileField(null=True)

    def __str__(self):
        return self.title




