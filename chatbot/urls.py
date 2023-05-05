from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name='home'),
    #path("<int:user_id>/chatbot/", views.chatbot_page, name="chatbot_page"),
    path("chatbot/", views.chatbot_page, name="chatbot_page"),
    path("anlysis-chatbot/", views.analysis_chatbot, name="analyse"),
    path("e-chatbot/", views.economy_chatbot, name="economy"),
    path("tl-chatbot/", views.trading_chatbot, name="trading"),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("delete/", views.delete_history, name="delete"),
    path('<pk>/delete/', views.TradingBotDeleteView.as_view(), name="delete_message"),
]
