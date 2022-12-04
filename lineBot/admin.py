from django.contrib import admin

# Register your models here.
from .models import LineChat, PhotoAlbum

admin.site.register(LineChat)
admin.site.register(PhotoAlbum)