from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200)
    phoneNumber = models.CharField(max_length=100)
    linkedIn = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username 

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    salary = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000)
    posted_by = models.ForeignKey("Profile", on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=timezone.now) 
    
   

    def __str__(self):
        return self.title  
