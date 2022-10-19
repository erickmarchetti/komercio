from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.UserListCreateView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("accounts/newest/<int:num>/", views.UserListByNumView.as_view()),
    path("accounts/<str:pk>/management/", views.UserUpdateActivityView.as_view()),
    path("accounts/<str:pk>/", views.UserUpdateView.as_view()),
]
