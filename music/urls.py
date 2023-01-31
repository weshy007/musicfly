from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login_user'),
    path('register/', views.register, name='register'),

]