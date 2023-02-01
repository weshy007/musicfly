from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('songs/(?P<filter_by>[a-zA-Z]+)/', views.songs, name='songs'),
    path('create_album/', views.create_album, name='create_album'),
    path('(?<album_id>[0-9]+)/', views.album_detail, name='detail'),
    path('(?P<album_id>[0-9]+)/delete_album/', views.delete_album, name='delete_album'),
    path('(?P<album_id>[0-9]+)/create_song/', views.upload_song, name='create_song'),
    path('(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/', views.delete_song, name='delete_song'),
    path('(?<song_id>[0-9]+)/favorite/', views.favorite, name='favorite'),
    path('(?P<album_id>[0-9]+)/favorite_album/', views.favorite_album, name='favorite_album'),

]