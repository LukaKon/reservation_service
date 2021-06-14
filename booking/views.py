from django.shortcuts import render, HttpResponse
from booking.models import Room
from django.views import View
from django.contrib import messages
from django.db.utils import IntegrityError
# Create your views here.


class Home(View):
    HTML_TEMPLATE = 'booking/room/home.html'

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
        # print(capacity, type(capacity))

        if name == '':
            # raise ValueError('Name is required.')
            # print('name error')
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'name_error': 'Name is required.'})

        room_list = [room.name for room in Room.objects.all()]
        if name in room_list:
            # raise IndentationError(f'Room {name} already exist.')
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'name_error': 'Name alredy exist.'})

        if isinstance(capacity, int):
            capacity = int(capacity)
        else:
            # raise ValueError(
            # f'Inserted value is not a integer: {type(capacity)}')
            return render(
                request,
                self.HTML_TEMPLATE,
                context={'capacity_error': 'Inserted value is not integer'})

        if capacity not in range(2, 400):
            # raise ValueError(
            #     f'Inserted negative value or to much (2-400): {capacity}.')
            return render(request,
                          self.HTML_TEMPLATE,
                          context={'capacity_error': f'(2-400): {capacity}'})

        Room.objects.create(name=name,
                            capacity=capacity,
                            projector_availability=projector_availability)
        messages.success(request, f'Room {name} added to DB.')
        return render(request, self.HTML_TEMPLATE)
