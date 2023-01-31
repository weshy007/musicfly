from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Q

from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song


# Create your views here.
def login(request):
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

        user = authenticate(username=username, password= password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'index.html', {'albums': albums})

    context = {
        "form": form
    }

    return render(request, 'register.html', context)


def logout(request):
    logout(request)
    form = UserForm(request.POST or None)

    context = {
        "form": form
    }

    return render(request, 'login.html', context)


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")

        if query:
            albums = albums.filter(
                Q(album_title__icontains = query) |
                Q(artist__icontains = query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icotains = query)
            ).distinct()

            context = {
                "albums": albums,
                "songs": song_results
            }

            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html', {"albums": albums})
