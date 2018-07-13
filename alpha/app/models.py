from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=255)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title +' '+self.body
class Coordonates(models.Model):
    lat=models.CharField(max_length=50)
    long=models.CharField(max_length=50)
    alt=models.CharField(max_length=50)
    moment=models.CharField(max_length=50)
    siteNumber=models.CharField(max_length=50)

class Site(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class myFiles(models.Model):
    pathOf=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    siteNumber=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)