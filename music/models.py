from django.db import models
from django.contrib.auth.models import Permission, User

# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250) # album_name
    genre = models.CharField(max_length=100)
    album_logo = models.FileField() # album_image
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE) # album_name
    song_title = models.CharField(max_length=100) # name
    audio_file = models.FileField(default='', upload_to='songs') # song
    song_image = models.FileField(upload_to='picture') # picture
    artist = models.CharField(max_length=255) # singer
    is_favorite = models.BooleanField(default=False) 

    def __str__(self):
        return self.song_title
