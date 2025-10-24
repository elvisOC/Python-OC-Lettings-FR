from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Modèle représentant une adresse physique.

    Attributs :
        number (PositiveIntegerField) :
            Numéro de la rue, maximum 9999.

        street (CharField) :
            Nom de la rue, longueur maximale 64 caractères.

        city (CharField) :
            Nom de la ville, longueur maximale 64 caractères.

        state (CharField) :
            Code de l'état, exactement 2 caractères.

        zip_code (PositiveIntegerField) :
            Code postal, maximum 99999.

        country_iso_code (CharField) :
            Code ISO du pays, exactement 3 caractères.

        verbose_name_plural :
            Corrige le pluriel de la classe Address.

    Méthodes :
        __str__() :
            Retourne une représentation textuelle de l'adresse (numéro + rue).
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f'{self.number} {self.street}'


class Letting(models.Model):
    """
    Modèle représentant une location immobilière.

    Attributs :
        title (CharField) : Titre de la location, longueur maximale 256 caractères.
        address (OneToOneField) : Adresse associée à la location.

    Méthodes :
        __str__() : Retourne le titre de la location.
    """
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
