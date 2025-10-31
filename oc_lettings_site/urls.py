"""
Configuration des URLs principales de l'application.
    Routes :
        '' : page d'accueil, handled par views.index
        'lettings/' : liste des locations, handled par lettings.views.index \n
        'lettings/<int:letting_id>/' : détails d'une location,handled par lettings.views.letting \n
        'profiles/' : liste des profils, handled par profiles.views.index \n
        'profiles/<str:username>/' : détails d'un profil, handled par profiles.views.profile \n
        'admin/' : interface d'administration Django
"""
from django.contrib import admin
from django.urls import path
import lettings.views
import profiles.views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', lettings.views.index, name='lettings_index'),
    path('lettings/<int:letting_id>/', lettings.views.letting, name='letting'),
    path('profiles/', profiles.views.index, name='profiles_index'),
    path('profiles/<str:username>/', profiles.views.profile, name='profile'),
    path('admin/', admin.site.urls),
]
