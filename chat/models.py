from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name
