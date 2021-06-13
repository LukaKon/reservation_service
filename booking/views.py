from django.shortcuts import render
from booking.models import Room
from django.views import View
# Create your views here.


class NewRoom(View):
    HTML_TEMPLATE = 'booking/room/new_room.html'

    def get(self, request):
        return render(request, self.HTML_TEMPLATE)
    def post(self, request):
        pass
