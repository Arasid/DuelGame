from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('points/', views.points, name='points'),
	path('add_duel/', views.add_duel, name='add_duel'),
    path('remove_duel/<int:duel_id>/', views.remove_duel, name='remove_duel'),
    path('login/', LoginView.as_view(template_name='game/login.html', redirect_field_name='index'), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
