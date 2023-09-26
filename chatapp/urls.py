from django.urls import path
from . import views

urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
	path('suggested-friends', views.SuggestedFriends.as_view(), name='suggested-friends'),
    path('online-users', views.GetOnlineUsers.as_view(), name='online-users'),
    path('start/chat', views.StartChat.as_view(), name='start-chat')
]