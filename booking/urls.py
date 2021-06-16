from django.urls import path
from . import views


app_name = 'booking'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('new/', views.NewRoom.as_view(), name='new_room'),
    path('all-rooms/', views.AllRooms.as_view(), name='all_rooms'),
    path('room-details/<int:room_id>',
         views.RoomDetails.as_view(), name='room-details'),
    path('edit-room/<int:room_id>', views.EditRoom.as_view(),
         name='edit_room'),
    path('delete-room/<int:room_id>',
         views.DeleteRoom.as_view(), name='delete_room'),
    # path('about/', views.AboutRoom.as_view(), name='about'),

    path('reserve-room/<int:room_id>', views.ReserveRoom.as_view(),
         name='reserve-room')
]
