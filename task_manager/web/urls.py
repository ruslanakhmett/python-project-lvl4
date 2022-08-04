from django.urls import path
from .views import IndexView, LoginPageView, SignUpView


urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', LoginPageView.as_view(), name='login'),
    path('users/create', SignUpView.as_view(), name='signup'),

]
