from django.http import JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']

# Create your views here.

def index(request):
    album = Album.objects.all()
    return render(request, 'index.html', {'album': album})


def songs(request):
    album_name = request.GET.get('album')
    songs_list = Song.objects.filter(album_name_id=album_name)
    paginator = Paginator(songs_list, 1)
    page_number = request.GET.get('page')
    songs_page = paginator.get_page(page_number)

    context = {
        'songs_page': songs_page,
        'album_name': album_name
    }

    return render(request, 'songs.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'index.html', {'albums': albums})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
            
    return render(request, 'login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'index.html', {'albums': albums})

    context = {
        "form": form
    }

    return render(request, 'register.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)

    context = {
        "form": form
    }

    return render(request, 'login.html', context)


# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#     else:
#         albums = Album.objects.filter(user=request.user)
#         song_results = Song.objects.all()
#         query = request.GET.get("q")

#         if query:
#             albums = albums.filter(
#                 Q(album_title__icontains=query) |
#                 Q(artist__icontains=query)
#             ).distinct()
#             song_results = song_results.filter(
#                 Q(song_title__icotains=query)
#             ).distinct()

#             context = {
#                 "albums": albums,
#                 "songs": song_results
#             }

#             return render(request, 'index.html', context)
#         else:
#             return render(request, 'index.html', {"albums": albums})


# def create_album(request):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#     else:
#         form = AlbumForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             album = form.save(commit=False)
#             album.user = request.user
#             album.album_logo = request.FILES['album_logo']
#             file_type = album.album_logo.url.split('.')[-1]
#             file_type = file_type.lower()
#             if file_type not in IMAGE_FILE_TYPES:
#                 context = {
#                     "album": album,
#                     "form": form,
#                     "error_message": 'Image file must be PNG, JPG, or JPEG'
#                 }
#                 return render(request, 'create_album.html', context)
#             album.save()
#             return render(request, 'detail.html', {"album": album})
#         context = {
#             "form": form,
#         }
#         return render(request, 'create_album.html', context)


# def album_detail(request, album_id):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#     else:
#         user = request.user
#         album = get_object_or_404(Album, pk=album_id)

#         context = {
#             "album": album,
#             "user": user
#         }
#         return render(request, 'detail.html', context)


# def delete_album(request, album_id):
#     album = Album.objects.get(pk=album_id)
#     album.delete()
#     albums = Album.objects.filter(user=request.user)
#     return render(request, 'index.html', {'albums': albums})


# def favorite(request, song_id):
#     song = get_object_or_404(Song, pk=song_id)
#     try:
#         if song.is_favorite:
#             song.is_favorite = False
#         else:
#             song.is_favorite = True
#         song.save()
#     except(KeyError, Song.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})


# def favorite_album(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         if album.is_favorite:
#             album.is_favorite = False
#         else:
#             album.is_favorite = True
#         album.save()
#     except (KeyError, Album.DoesNotExist):
#         return JsonResponse({"success": False})
#     else:
#         return JsonResponse({"success": True})


# def songs(request, filter_by):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#     else:
#         try:
#             song_ids = []
#             for album in Album.objects.filter(user=request.user):
#                 for song in album.song_set.all():
#                     song_ids.append(song.pk)
#             user_songs = Song.objects.filter(pk__in=song_ids)
#             if filter_by == 'favorites':
#                 user_songs = user_songs.filter(is_favorite=True)
#         except Album.DoesNotExist:
#             user_songs = []

#         context = {
#             "song_list": user_songs,
#             "filter_by": filter_by
#         }

#         return render(request, 'songs.html', context)


# def play_song(request, song_id):
#     song = Song.objects.get(id=song_id)
#     audio_file = song.audio_file.path
#     return FileResponse(open(audio_file, 'rb'))


# def upload_song(request, album_id):
#     form = SongForm(request.POST or None, request.FILES or None)
#     album = get_object_or_404(Album, pk=album_id)
#     if form.is_valid():
#         album_songs = album.song_set.all()
#         for s in album_songs:
#             if s.song_title == form.cleaned_data.get("song_title"):
#                 context = {
#                     "album": album,
#                     "form": form,
#                     "error_message": 'You already added that song'
#                 }
#                 return render(request, "create_song.html", context)

#         song = form.save(commit=False)
#         song.album = album
#         song.audio_file = request.FILES['audio_file']
#         file_type = song.audio_file.url.split('.')[-1]
#         file_type = file_type.lower()

#         if file_type not in AUDIO_FILE_TYPES:
#             context = {
#                 'album': album,
#                 'form': form,
#                 'error_message': 'Audio file must be WAV, MP3, or OGG',
#             }
#             return render(request, 'create_song.html', context)
#         song.save()
#         return render(request, 'detail.html', {"album": album})
#     context = {
#         'album': album,
#         'form': form,
#     }
#     return render(request, 'create_song.html', context)


# def delete_song(request, album_id, song_id):
#     album = get_object_or_404(Album, pk=album_id)
#     song = Song.objects.get(pk=song_id)
#     song.delete()
#     return render(request, 'detail.html', {"album": album})
