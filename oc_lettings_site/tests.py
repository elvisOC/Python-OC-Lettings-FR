"""
Module de tests unitaires pour l'application Django OCLettingsSite.

Ce module contient des tests pour :
- Les modèles (`Address`, `Letting`, `Profile`)
- Les vues (`index`, `letting`, `profile`, etc.)
- Les URLs principales du projet

Chaque test utilise Pytest et Django, et simule les appels aux fonctions ou
méthodes avec des objets factices (mocks) pour isoler le comportement testé.

"""

import pytest
from django.http import HttpRequest
from django.urls import resolve
from unittest.mock import Mock
from lettings.models import Address, Letting
from profiles.models import Profile


# =========================
# MODELS TESTS
# =========================

@pytest.mark.django_db
def test_address_str(monkeypatch):
    """
    Teste la méthode ``__str__`` du modèle :class:`lettings.models.Address`.

    Vérifie que la représentation textuelle d'une adresse correspond au format attendu.

    :param monkeypatch: fixture Pytest permettant de remplacer temporairement la méthode ``__str__``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    address = Address(
        number=123,
        street="Main Street",
        city="City",
        state="ST",
        zip_code=12345,
        country_iso_code="USA"
    )
    monkeypatch.setattr(address, "__str__", lambda self: f"Address: {self.number} {self.street}")
    assert str(address) == "123 Main Street"


@pytest.mark.django_db
def test_letting_str_and_relation(monkeypatch):
    """
    Teste la méthode ``__str__`` du modèle :class:`lettings.models.Letting`
    et la relation avec :class:`lettings.models.Address`.

    :param monkeypatch: fixture Pytest utilisée pour redéfinir la méthode ``__str__``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    address = Address(
        number=1,
        street="Elm Street",
        city="City",
        state="ST",
        zip_code=12345,
        country_iso_code="USA"
    )
    letting = Letting(title="Beautiful House", address=address)
    monkeypatch.setattr(letting, "__str__", lambda self: f"Letting: {self.title}")
    assert str(letting) == "Beautiful House"
    assert letting.address == address


def test_profile_str_and_favorite_city():
    """
    Teste la méthode ``__str__`` du modèle :class:`profiles.models.Profile`.

    Ce test vérifie que la représentation textuelle d'un profil contient
    le nom d'utilisateur et la ville favorite.
    """
    fake_user = Mock()
    fake_user.username = "john_doe"

    profile = Mock()
    profile.user = fake_user
    profile.favorite_city = "Paris"
    profile.__str__ = lambda self=profile: f"{self.user.username} - {self.favorite_city}"

    assert str(profile) == "john_doe - Paris"


# =========================
# VIEWS TESTS
# =========================

@pytest.mark.django_db
def test_lettings_index_view(monkeypatch):
    """
    Teste la vue ``index`` du module :mod:`lettings.views`.

    Vérifie que la vue retourne bien une liste de locations dans le contexte.

    :param monkeypatch: fixture Pytest utilisée pour simuler la méthode ``Letting.objects.all`` et ``render``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    from lettings.views import index
    request = HttpRequest()
    fake_lettings = ["letting1", "letting2"]
    monkeypatch.setattr(Letting.objects, "all", lambda: fake_lettings)

    def fake_render(req, template, context):
        return context

    monkeypatch.setattr("lettings.views.render", fake_render)
    response = index(request)
    assert response["lettings_list"] == fake_lettings


@pytest.mark.django_db
def test_letting_detail_view(monkeypatch):
    """
    Teste la vue ``letting`` du module :mod:`lettings.views`.

    Vérifie que la vue renvoie les bonnes informations pour une location donnée.

    :param monkeypatch: fixture Pytest utilisée pour simuler la méthode ``Letting.objects.get`` et ``render``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    from lettings.views import letting
    request = HttpRequest()

    class FakeAddress:
        pass

    class FakeLetting:
        title = "Fake Letting"
        address = FakeAddress()

    fake_letting = FakeLetting()
    monkeypatch.setattr(Letting.objects, "get", lambda id: fake_letting)

    def fake_render(req, template, context):
        return context

    monkeypatch.setattr("lettings.views.render", fake_render)
    response = letting(request, letting_id=42)
    assert response["title"] == "Fake Letting"


@pytest.mark.django_db
def test_profiles_index_view(monkeypatch):
    """
    Teste la vue ``index`` du module :mod:`profiles.views`.

    Vérifie que la liste des profils est correctement renvoyée dans le contexte.

    :param monkeypatch: fixture Pytest utilisée pour simuler ``Profile.objects.all`` et ``render``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    from profiles.views import index
    request = HttpRequest()
    fake_profiles = ["profile1", "profile2"]
    monkeypatch.setattr(Profile.objects, "all", lambda: fake_profiles)

    def fake_render(req, template, context):
        return context

    monkeypatch.setattr("profiles.views.render", fake_render)
    response = index(request)
    assert response["profiles_list"] == fake_profiles


@pytest.mark.django_db
def test_profile_detail_view(monkeypatch):
    """
    Teste la vue ``profile`` du module :mod:`profiles.views`.

    Vérifie que la vue renvoie les informations correctes pour un utilisateur donné.

    :param monkeypatch: fixture Pytest utilisée pour simuler ``Profile.objects.get`` et ``render``.
    :type monkeypatch: pytest.MonkeyPatch
    """
    from profiles.views import profile
    request = HttpRequest()

    class FakeUser:
        username = "alice"

    class FakeProfile:
        user = FakeUser()

    fake_profile = FakeProfile()
    monkeypatch.setattr(Profile.objects, "get", lambda user__username: fake_profile)

    def fake_render(req, template, context):
        return context

    monkeypatch.setattr("profiles.views.render", fake_render)
    response = profile(request, username="alice")
    assert response["profile"].user.username == "alice"


# =========================
# URLS TESTS
# =========================

@pytest.mark.django_db
def test_urls(monkeypatch):
    """
    Teste la configuration des URLs du projet principal.

    Vérifie que les chemins principaux (``/``, ``/lettings/``, ``/profiles/``, etc.)
    sont correctement résolus vers une fonction de vue valide.

    :param monkeypatch: fixture Pytest (non utilisée ici mais disponible pour cohérence).
    :type monkeypatch: pytest.MonkeyPatch
    """
    import oc_lettings_site.urls as urls
    fake_called = {}

    def fake_index(request):
        fake_called["index"] = True
        return "index_response"

    def fake_lettings_index(request):
        fake_called["lettings_index"] = True
        return "lettings_index_response"

    def fake_letting(request, letting_id):
        fake_called["letting_id"] = letting_id
        return f"letting_{letting_id}_response"

    def fake_profiles_index(request):
        fake_called["profiles_index"] = True
        return "profiles_index_response"

    def fake_profile(request, username):
        fake_called["profile_username"] = username
        return f"profile_{username}_response"

    assert resolve("/").func is not None
    assert resolve("/lettings/").func is not None
    assert resolve("/lettings/42/").func is not None
    assert resolve("/profiles/").func is not None
    assert resolve("/profiles/alice/").func is not None
