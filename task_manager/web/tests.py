from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse

from .views import UpdateUserView, DeleteUserView
from .models import Labels, Statuses, Tasks


ROOT_URL = "http://127.0.0.1:8000"


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CheckStatusCodeNoLoginTestCases(TestCase):

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
        response = self.client.get(ROOT_URL + "/statuses/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/statuses/create/")
        self.assertEqual(response.status_code, 302)
        # response = self.client.get(ROOT_URL + "/tasks/")
        # self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/tasks/create/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/labels/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(ROOT_URL + "/labels/create/")
        self.assertEqual(response.status_code, 302)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CheckStatusCodeYesLoginTestCases(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'sergio',
            'password': '12345test'}
        User.objects.create_user(**self.credentials)
        self.client.login(username='sergio', password='12345test')

    def test_200_response_status_code(self):
        response = self.client.get(ROOT_URL + "/statuses/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/statuses/create/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/tasks/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/tasks/create/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/labels/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(ROOT_URL + "/labels/create/")
        self.assertEqual(response.status_code, 200)



@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class LogInLogOutTestCases(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'sergio',
            'password': '12345test'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        response = self.client.post("/logout/", follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class UserPagesTestCases(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'sergio',
            'password': '12345test'}
        User.objects.create_user(**self.credentials)
        self.client.login(username='sergio', password='12345test')

    def test_allowed_user_update_page(self):
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.get("/users/1/update/", kwargs=kwargs)
        request.user = User.objects.get(username="sergio")
        response = UpdateUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_user_update_page(self):
        kwargs = {"pk": 2}
        factory = RequestFactory()
        request = factory.get("/users/1/update/", kwargs=kwargs)
        request.user = User.objects.get(username="sergio")
        response = UpdateUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_allowed_user_delete_page(self):
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.get("/users/1/delete/", kwargs=kwargs)
        request.user = User.objects.get(username="sergio")
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_user_delete_page(self):
        kwargs = {"pk": 2}
        factory = RequestFactory()
        request = factory.get("/users/1/delete/", kwargs=kwargs)
        request.user = User.objects.get(username="sergio")
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        kwargs = {"pk": 1}
        factory = RequestFactory()
        request = factory.post("/users/1/delete/", kwargs=kwargs)
        request.user = User.objects.get(username="sergio")
        response = DeleteUserView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        user_exist = User.objects.filter(username="sergio").count()
        self.assertEqual(user_exist, False)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CreateTestCases(TestCase):

    def setUp(self):
        self.client = Client()
        self.labels_url = reverse('labels_create')
        self.statuses_url = reverse('statuses_create')
        self.credentials = {
            'username': 'sergio',
            'password': '12345test'}
        User.objects.create_user(**self.credentials)
        self.client.login(username='sergio', password='12345test')

    def test_create_label(self):
        response = self.client.post(self.labels_url,data={
            'name': 'label1'
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Labels.objects.get(id=1).name, 'label1')

    def test_create_status(self):
        response = self.client.post(self.statuses_url, data={
            'name': 'status1'
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Statuses.objects.get(id=1).name, 'status1')


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CreateTaskTestCases(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task_url = reverse('tasks_create')
        self.credentials = {
            'username': 'sergio',
            'password': '12345test'}
        User.objects.create_user(**self.credentials)
        self.client.login(username='sergio', password='12345test')
        Statuses.objects.bulk_create([Statuses(name='status1'), Statuses(name='status2')])
        Labels.objects.bulk_create([Labels(name='label1'), Labels(name='label2')])


    def test_create_and_update_task(self):

        response = self.client.post(self.task_url, data={
            'name': 'task1',
            'description': 'description1',
            'status': 1,
            'executor': 'sergio',
            'labels': ['label1']})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Tasks.objects.get(id=1).name, 'task1')
        self.assertEquals(Tasks.objects.get(id=1).description, 'description1')
        self.assertEquals(Tasks.objects.get(id=1).creator_id, 1)
        self.assertEquals(Tasks.objects.get(id=1).executor_id, 1)
        self.assertEquals(Tasks.objects.get(id=1).status_id, 1)
