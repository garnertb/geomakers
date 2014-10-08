from django.db import models

class Profile(models.Model):
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.URLField(default="", null=True, blank=True)
    twitter = models.URLField(default="", null=True, blank=True)
    linkedin = models.URLField(default="", null=True, blank=True)

class Tag(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

class Link(models.Model):
    link = models.URLField(null=True, blank=True)

class Video(models.Model):
    url = models.URLField(null=True, blank=True)

class MakerSpace(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    lat = models.DecimalField(max_digits=8, decimal_places=5)
    lon = models.DecimalField(max_digits=8, decimal_places=5)
    url = models.URLField(default="", null=True, blank=True)
