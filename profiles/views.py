from django.shortcuts import render
from .models import Profile


def index(request):
    """
    Vue qui affiche la liste de tous les profils.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La réponse contenant le template 'profiles/index.html'
                      avec le contexte {'profiles_list': profiles_list}.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """
    Vue qui affiche les détails d'un profil spécifique en fonction du nom d'utilisateur.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        username (str): Le nom d'utilisateur associé au profil.

    Returns:
        HttpResponse: La réponse contenant le template 'profiles/profile.html'
                      avec le contexte {'profile': profile}.
    """
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
