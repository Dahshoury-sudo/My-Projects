from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Create Database tables here


class User(AbstractUser):
    name = models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True,unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")


    USERNAME_FIELD = 'email'   # That line means when u log in use email and not username
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) # choose the room user for the User Class which is built in django, ONE TO MANY Relation
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) # choose the room topic for the Topic Class, ONE TO MANY Relation
    name = models.CharField(max_length=200) # Thats a text
    description = models.TextField(null = True, blank= True) # thats a bigger text and can be null
    updated = models.DateTimeField(auto_now=True) # thats a date data type this runs everytime we call a save() method
    created = models.DateTimeField(auto_now_add=True) # thats a date data type this runs only one time which is the time we created the instance, MANY TO MANY Relation
    participants = models.ManyToManyField(User,related_name='participants',blank=True)

    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.name



class Message(models.Model): #message is a child from room
    user = models.ForeignKey(User,on_delete=models.CASCADE) # User is the parent and Message is the child
    room = models.ForeignKey(Room,on_delete=models.CASCADE) # one to many relationship Room is the parent and Message is the child
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # thats a date data type this runs everytime we call a save() method
    created = models.DateTimeField(auto_now_add=True) # thats a date data type this runs only one time which is the time we created the instance

    class Meta:
        ordering = ['-created','-updated']
    def __str__(self):
        return self.body[0:50]
    

