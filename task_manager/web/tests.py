from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase, override_settings

from .views import UpdateUserView

ROOT_URL = "http://127.0.0.1:8000"


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class NoLoginTestCase(TestCase):
    def test_without_login(self):

        response = self.client.get(ROOT_URL)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/login/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/users/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/users/create/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/users/1/update/")
        self.assertEqual(response.status_code, 302)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="sergio",
            first_name="Сергей",
            last_name="Иванов",
            password="12345test",
        )

    def test_login_logout(self):
        client = Client()
        response = client.post(
            "/login/", {"username": "sergio", "password": "12345test"}
        )
        self.assertEqual(response.status_code, 200)
        response = client.post("/logout/")
        self.assertEqual(response.status_code, 302)

    def test_allowed_user_update_page(self):
        user = User.objects.get(username="sergio")
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.get("/users/1/update/", kwargs=kwargs)
        request.user = user
        response = UpdateUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_user_update_page(self):
        user = User.objects.get(username="sergio")
        kwargs = {"pk": 2}
        factory = RequestFactory()
        request = factory.get("/users/1/update/", kwargs=kwargs)
        request.user = user
        response = UpdateUserView.as_view()(request, **kwargs)
        self.assertNotEqual(response.status_code, 200)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="sergio",
            first_name="Сергей",
            last_name="Иванов",
            password="12345test",
        )

    def test_username(self):
        user = User.objects.get(id=1)
        recorded_name = user.username
        self.assertEqual(recorded_name, "sergio")

    def test_first_name(self):
        user = User.objects.get(id=1)
        recorded_name = user.first_name
        self.assertEqual(recorded_name, "Сергей")

    def test_last_name(self):
        user = User.objects.get(id=1)
        recorded_name = user.last_name
        self.assertEqual(recorded_name, "Иванов")
