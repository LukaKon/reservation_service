from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector_availability = models.BooleanField()

    def __str__(self):
        return f'{self.name}: {self.capacity}, {self.projector_availability}'


class N(models.Model):
    pass
