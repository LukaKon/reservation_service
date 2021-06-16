from django.db import models
# from django.db.models.deletion import CASCADE


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector_availability = models.BooleanField()

    def __str__(self):
        return f'{self.name}: {self.capacity}, {self.projector_availability}'


class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'room_id',)

    def __str__(self):
        return f'{self.date}: {self.room_id}, {self.comment}'
