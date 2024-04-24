from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User 

# Create your models here.


#Guest = Movie - Reservation
class Movie(models.Model):
    hall = models.CharField( max_length=10)
    name_movie = models.CharField( max_length=10)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name_movie

class Guest(models.Model):
    name = models.CharField( max_length=15)
    mobile = models.CharField( max_length=11)
    def __str__(self):
        return self.name
    
    
    
class Reservation(models.Model):
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE,related_name='reservation')    
    movie = models.ForeignKey(Movie,on_delete=models.DO_NOTHING,related_name='movie') 
    # def __str__(self):
    #     return self.guest.name    
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=50)
    body = models.TextField()
    def __str__(self):
        return self.title
    
@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def token_create(sender,instance , created,**kwargs):
    if created:
        Token.objects.create(user = instance)   