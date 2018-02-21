from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('points/', views.points, name='points'),
	path('add_duel/', views.add_duel, name='add_duel'),
	path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
