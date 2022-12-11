from django.db import models

# Create your models here.

class LineChat(models.Model):
    groupId = models.CharField(max_length=100)
    userId = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    text = models.TextField(blank=True)
    photoid = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class ChannelInfo(models.Model):
    groupId = models.CharField(max_length=100)
    imgurAlbum = models.CharField(max_length=20, default='')
    alias = models.CharField(max_length=20, default='')

class PhotoAlbum(models.Model):
    groupId = models.CharField(max_length=100)
    userId = models.CharField(max_length=100)
    album = models.CharField(max_length=20)
    imgurId = models.CharField(max_length=100)
    photoDate = models.CharField(max_length=10)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)