from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Modèle représentant le profil utilisateur.

    Attributs :
        user (OneToOneField) : Utilisateur lié à ce profil.
        favorite_city (CharField) : Ville favorite de l'utilisateur
        (optionnelle, max 64 caractères).

    Méthodes :
        __str__() : Retourne le nom d'utilisateur associé.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profiles_profile"
    )
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
