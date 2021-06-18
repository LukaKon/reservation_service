from django.shortcuts import render, redirect
from booking.models import Room, Reservation
from django.views import View
from django.contrib import messages
from django.db.utils import IntegrityError
import datetime
from . import models
# Create your views here.


class Home(View):
    HTML_TEMPLATE = 'booking/room/home.html'

    def get(self, request):
        return render(request, self.HTML_TEMPLATE)


class About(View):
    # TODO: about.html is empty
    HTML_TEMPLATE = 'booking/room/about.html'

    def get(self, request):
        return render(request, self.HTML_TEMPLATE)


class NewRoom(View):
    HTML_TEMPLATE = 'booking/room/new_room.html'

    def get(self, request):
        return render(request, self.HTML_TEMPLATE)

    def post(self, request):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector_availability = request.POST.get(
            'projector_availability') == 'on'

        if name == '':
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'name_error': 'Name is required.'})

        room_list = [room.name for room in Room.objects.all()]
        if name in room_list:
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'name_error': 'Name alredy exist.'})

        if not int(capacity):
            return render(
                request,
                self.HTML_TEMPLATE,
                context={'capacity_error': 'Inserted value is not integer'})
        else:
            capacity = int(capacity)

        if capacity not in range(2, 400):
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'capacity_error': f'(2-400): {capacity}'})

        Room.objects.create(name=name,
                            capacity=capacity,
                            projector_availability=projector_availability)
        messages.success(request, f'Room {name} added to DB.')
        # return render(request, self.HTML_TEMPLATE)
        return redirect('booking:all_rooms')


class AllRooms(View):
    HTML_TEMPLATE = 'booking/room/all_rooms.html'

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        reservations = Reservation.objects.all()
        if not rooms:  # TODO: not tested yet
            return render(request, self.HTML_TEMPLATE, context={'empty': True})
        return render(
            request,
            self.HTML_TEMPLATE,
            context={
                'rooms': rooms,
                'reservations': reservations
            },
        )


class RoomDetails(View):
    HTML_TEMPLATE = 'booking/room/room_details.html'

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reservations = Reservation.objects.filter(
            room_id=room).order_by('-date')
        return render(request,
                      self.HTML_TEMPLATE,
                      context={
                          'room': room,
                          'reservations': reservations,
                      })


class EditRoom(View):
    HTML_TEMPLATE = 'booking/room/new_room.html'

    def get(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(pk=room_id)
        print(room)
        return render(request, self.HTML_TEMPLATE, context={'room': room})

    def post(self, request, room_id):

        current_room = Room.objects.get(pk=room_id).name
        room_list = [room.name for room in Room.objects.all()]

        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector_availability = request.POST.get(
            'projector_availability') == 'on'

        if name == '':
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'name_error': 'Name is required.',
                              'room': current_room
                          })

        room_list.remove(current_room)
        if name in room_list:
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'name_error': 'Name alredy exist.',
                              'room': current_room
                          })

        if not int(capacity):
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'capacity_error':
                              'Inserted value is not integer',
                              'room': current_room
                          })
        else:
            capacity = int(capacity)

        if capacity not in range(2, 400):
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'capacity_error': f'(2-400): {capacity}',
                              'room': current_room
                          })

        room = Room.objects.get(pk=room_id)
        room.name = name
        room.capacity = capacity
        room.projector_availability = projector_availability
        room.save()

        messages.success(request, 'Room data have been updated')
        return redirect('booking:all_rooms')


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()

        messages.success(request, f'Room {room.name} has been deleted.')
        return redirect('booking:all_rooms')


class ReserveRoom(View):
    HTML_TEMPLATE = 'booking/room/reserve.html'

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, self.HTML_TEMPLATE, context={'room': room})

    def post(self, request, room_id):
        date = request.POST.get('date')
        comment = request.POST.get('comment')

        room = Room.objects.get(pk=room_id)
        conv_date = datetime.datetime.strptime(date, '%Y-%m-%d')

        if Reservation.objects.filter(room_id=room_id,
                                      date=conv_date).exists():
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'date_error': 'Room already reserved.',
                              'room': room
                          })

        if conv_date < datetime.datetime.now():
            return render(request,
                          self.HTML_TEMPLATE,
                          context={
                              'date_error': 'Are you time traveler?',
                              'room': room,
                          })

        Reservation.objects.create(
            date=date,
            room_id=room,
            comment=comment,
        )

        messages.success(request,
                         f'Reservation for room "{room.name}" is done.')
        return redirect('booking:all_rooms')
