from django.urls import path

from .views import (DeleteUserView, IndexView, LoginPageView, LogoutView,
                    SignUpView, UpdateUserView, UsersShowView, StatusesShowView,
                    StatusesCreateView, StatusesUpdateView, StatusesDeleteView, TasksListView,
                    TasksCreateView, TasksUpdateView, TasksDeleteView, TaskDetailsShowView,
                    LabelsView, LabelsCreateView, LabelsUpdateView, LabelsDeleteView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('users/', UsersShowView.as_view(), name='users'),
    path('users/create/', SignUpView.as_view(), name='signup'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    path('statuses/', StatusesShowView.as_view(), name='statuses'),
    path('statuses/create/', StatusesCreateView.as_view(), name='statuses_create'),
    path('statuses/<int:pk>/update/', StatusesUpdateView.as_view(), name='statuses_update'),
    path('statuses/<int:pk>/delete/', StatusesDeleteView.as_view(), name='statuses_delete'),

    path('tasks/', TasksListView.as_view(), name='tasks'),
    path('tasks/create/', TasksCreateView.as_view(), name='tasks_create'),
    path('tasks/<int:pk>/', TaskDetailsShowView.as_view(), name='tasks_show'),
    path('tasks/<int:pk>/update/', TasksUpdateView.as_view(), name='tasks_update'),
    path('tasks/<int:pk>/delete/', TasksDeleteView.as_view(), name='tasks_delete'),

    path('labels/', LabelsView.as_view(), name='labels'),
    path('labels/create/', LabelsCreateView.as_view(), name='labels_create'),
    path('labels/<int:pk>/update/', LabelsUpdateView.as_view(), name='labels_update'),
    path('labels/<int:pk>/delete/', LabelsDeleteView.as_view(), name='labels_delete'),

]
