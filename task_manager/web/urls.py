from django.urls import path

from .views import (DeleteUserView, IndexView, LoginPageView, LogoutView,
                    SignUpView, UpdateUserView, UsersShowView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UsersShowView.as_view(), name='users'),
    path('users/create/', SignUpView.as_view(), name='signup'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

]
