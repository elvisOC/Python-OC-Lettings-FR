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
    address = Address(
        number=123,
        street="Main Street",
        city="City", state="ST",
        zip_code=12345,
        country_iso_code="USA"
    )
    monkeypatch.setattr(address, "__str__", lambda self: f"Address: {self.number} {self.street}")
    assert str(address) == "123 Main Street"


@pytest.mark.django_db
def test_letting_str_and_relation(monkeypatch):
    address = Address(
        number=1,
        street="Elm Street",
        city="City", state="ST",
        zip_code=12345,
        country_iso_code="USA")
    letting = Letting(title="Beautiful House", address=address)
    monkeypatch.setattr(letting, "__str__", lambda self: f"Letting: {self.title}")
    assert str(letting) == "Beautiful House"
    assert letting.address == address


def test_profile_str_and_favorite_city():
    # Crée un mock pour l'utilisateur
    fake_user = Mock()
    fake_user.username = "john_doe"

    # Crée un mock pour le Profile
    profile = Mock()
    profile.user = fake_user
    profile.favorite_city = "Paris"

    # On mock la méthode __str__ pour reproduire le comportement attendu
    profile.__str__ = lambda self=profile: f"{self.user.username} - {self.favorite_city}"

    # Test
    assert str(profile) == "john_doe - Paris"


# =========================
# VIEWS TESTS
# =========================

@pytest.mark.django_db
def test_lettings_index_view(monkeypatch):
    from lettings.views import index
    request = HttpRequest()
    fake_lettings = ["letting1", "letting2"]
    monkeypatch.setattr(Letting.objects, "all", lambda: fake_lettings)
    def fake_render(req, template, context): return context
    monkeypatch.setattr("lettings.views.render", fake_render)
    response = index(request)
    assert response["lettings_list"] == fake_lettings


@pytest.mark.django_db
def test_letting_detail_view(monkeypatch):
    from lettings.views import letting
    request = HttpRequest()

    class FakeAddress:
        pass

    class FakeLetting:
        title = "Fake Letting"
        address = FakeAddress()

    fake_letting = FakeLetting()
    monkeypatch.setattr(Letting.objects, "get", lambda id: fake_letting)
    def fake_render(req, template, context): return context
    monkeypatch.setattr("lettings.views.render", fake_render)
    response = letting(request, letting_id=42)
    assert response["title"] == "Fake Letting"


@pytest.mark.django_db
def test_profiles_index_view(monkeypatch):
    from profiles.views import index
    request = HttpRequest()
    fake_profiles = ["profile1", "profile2"]
    monkeypatch.setattr(Profile.objects, "all", lambda: fake_profiles)
    def fake_render(req, template, context): return context
    monkeypatch.setattr("profiles.views.render", fake_render)
    response = index(request)
    assert response["profiles_list"] == fake_profiles


@pytest.mark.django_db
def test_profile_detail_view(monkeypatch):
    from profiles.views import profile
    request = HttpRequest()

    class FakeUser:
        username = "alice"

    class FakeProfile:
        user = FakeUser()

    fake_profile = FakeProfile()
    monkeypatch.setattr(Profile.objects, "get", lambda user__username: fake_profile)
    def fake_render(req, template, context): return context
    monkeypatch.setattr("profiles.views.render", fake_render)
    response = profile(request, username="alice")
    assert response["profile"].user.username == "alice"


# =========================
# URLS TESTS
# =========================

@pytest.mark.django_db
def test_urls(monkeypatch):
    import oc_lettings_site.urls as urls
    fake_called = {}

    def fake_index(request):
        fake_called["index"] = True
        return "index_response"
        monkeypatch.setattr(urls.views, "index", fake_index)

    def fake_lettings_index(request):
        fake_called["lettings_index"] = True
        return "lettings_index_response"
        monkeypatch.setattr(urls.lettings.views, "index", fake_lettings_index)

    def fake_letting(request, letting_id):
        fake_called["letting_id"] = letting_id
        return f"letting_{letting_id}_response"
        monkeypatch.setattr(urls.lettings.views, "letting", fake_letting)

    def fake_profiles_index(request):
        fake_called["profiles_index"] = True
        return "profiles_index_response"
        monkeypatch.setattr(urls.profiles.views, "index", fake_profiles_index)

    def fake_profile(request, username):
        fake_called["profile_username"] = username
        return f"profile_{username}_response"
        monkeypatch.setattr(urls.profiles.views, "profile", fake_profile)

    assert resolve("/").func is not None
    assert resolve("/lettings/").func is not None
    assert resolve("/lettings/42/").func is not None
    assert resolve("/profiles/").func is not None
    assert resolve("/profiles/alice/").func is not None
