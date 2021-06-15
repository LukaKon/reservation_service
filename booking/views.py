from django.shortcuts import render, redirect, HttpResponse
from booking.models import Room
from django.views import View
from django.contrib import messages
from django.db.utils import IntegrityError
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

        if isinstance(capacity, int):
            capacity = int(capacity)
        else:
            return render(
                request,
                self.HTML_TEMPLATE,
                context={'capacity_error': 'Inserted value is not integer'})

        if capacity not in range(2, 400):
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'capacity_error': f'(2-400): {capacity}'})

        Room.objects.create(name=name,
                            capacity=capacity,
                            projector_availability=projector_availability)
        messages.success(request, f'Room {name} added to DB.')
        return render(request, self.HTML_TEMPLATE)


class AllRooms(View):
    HTML_TEMPLATE = 'booking/room/all_rooms.html'

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        return render(request,
                      self.HTML_TEMPLATE,
                      context={'rooms': rooms})

    def post(self, request):
        pass


class RoomDetails(View):
    HTML_TEMPLATE = 'booking/room/room_details.html'

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request,
                      self.HTML_TEMPLATE,
                      context={'room': room})


class EditRoom(View):
    HTML_TEMPLATE = 'booking/room/edit_room.html'
    HTML_REDIRECT = 'booking/room/all_rooms.html'

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request,
                      self.HTML_TEMPLATE,
                      context={'room': room})

    def post(self, request, room_id):

        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector_availability = request.POST.get(
            'projector_availability') == 'on'

        room = Room.objects.get(pk=room_id)

        room.name = name
        room.capacity = capacity
        room.projector_availability = projector_availability
        room.save()

        messages.success(request, 'Room data have been updated')
        return redirect(self.HTML_REDIRECT)


class DeleteRoom(View):
    HTML_REDIRECT = 'booking/room/all_rooms.html'

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()

        messages.success(request, f'Room {room.name} has been deleted.')
        return redirect(self.HTML_REDIRECT)
