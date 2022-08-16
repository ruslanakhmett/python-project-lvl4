from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase, override_settings

from .views import UpdateUserView, DeleteUserView

ROOT_URL = "http://127.0.0.1:8000"


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class WithoutLoginTestCases(TestCase):

    def test_200_response_status_code(self):

        response = self.client.get(ROOT_URL)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/login/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/users/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/users/create/")
        self.assertEqual(response.status_code, 200)

    def test_302_response_status_code(self):
        response = self.client.get(ROOT_URL + "/users/1/update/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/users/1/delete/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/statuses/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/statuses/create/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/statuses/1/update/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/tasks/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/tasks/create/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/tasks/1/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/labels/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/labels/create/")
        self.assertEqual(response.status_code, 302)



    def test_login_logout(self):
        client = Client()
        response = client.post(
            "/login/", {"username": "sergio", "password": "12345test"}
        )
        self.assertEqual(response.status_code, 200)
        response = client.post("/logout/")
        self.assertEqual(response.status_code, 302)



@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class WithLoginTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="sergio",
            first_name="Сергей",
            last_name="Иванов",
            password="12345test",
        )

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
        self.assertEqual(response.status_code, 302)

    def test_allowed_user_delete_page(self):
        user = User.objects.get(username="sergio")
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.get("/users/1/delete/", kwargs=kwargs)
        request.user = user
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_user_delete_page(self):
        user = User.objects.get(username="sergio")
        kwargs = {"pk": 2}
        factory = RequestFactory()
        request = factory.get("/users/1/delete/", kwargs=kwargs)
        request.user = user
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        user = User.objects.get(username="sergio")
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.post("/users/1/delete/", kwargs=kwargs)
        request.user = user
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        user_exist = User.objects.filter(username="sergio").count()
        self.assertEqual(user_exist, False)











# class UserModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         User.objects.create(
#             username="sergio",
#             first_name="Сергей",
#             last_name="Иванов",
#             password="12345test",
#         )

#     def test_username(self):
#         user = User.objects.get(id=1)
#         recorded_name = user.username
#         self.assertEqual(recorded_name, "sergio")

#     def test_first_name(self):
#         user = User.objects.get(id=1)
#         recorded_name = user.first_name
#         self.assertEqual(recorded_name, "Сергей")

#     def test_last_name(self):
#         user = User.objects.get(id=1)
#         recorded_name = user.last_name
#         self.assertEqual(recorded_name, "Иванов")
