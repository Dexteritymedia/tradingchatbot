from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("anlysis-chatbot/", views.analysis_chatbot, name="analyse"),
    path("e-chatbot/", views.economy_chatbot, name="economy"),
    path("tl-chatbot/", views.trading_chatbot, name="trading"),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
