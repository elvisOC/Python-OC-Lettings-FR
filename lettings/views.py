from django.shortcuts import render
from .models import Letting


def index(request):
    """
    Vue qui affiche la liste de toutes les locations.

    Args:
        request (HttpRequest): La requête HTTP reçue.

    Returns:
        HttpResponse: La réponse contenant le template 'lettings/index.html'
                      avec le contexte {'lettings_list': lettings_list}.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """
    Vue qui affiche les détails d'une location spécifique.

    Args:
        request (HttpRequest): La requête HTTP reçue.
        letting_id (int): L'identifiant de la location.

    Returns:
        HttpResponse: La réponse contenant le template 'lettings/letting.html'
                      avec le contexte {'title': letting.title, 'address': letting.address}.
    """
    letting = Letting.objects.get(id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
