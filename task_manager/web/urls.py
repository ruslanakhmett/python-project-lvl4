from django.urls import path
from .views import IndexView, LoginPageView, SignUpView, LogoutView, UsersShowView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('users/create', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UsersShowView.as_view(), name='users'),

]
