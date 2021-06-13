from django.urls import path
from . import views


app_name = 'booking'

urlpatterns = [
    path('new/', views.NewRoom.as_view(), name='new_room'),
]
