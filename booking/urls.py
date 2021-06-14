from django.urls import path
from . import views


app_name = 'booking'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('new/', views.NewRoom.as_view(), name='new_room'),
]
