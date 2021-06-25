from django.db import models

class LocationCoordinates(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    coordinates = models.CharField(max_length=100, default="UNAVAILABLE")

    def GetCoordinates(self):
        return str(self.coordinates)

    def __str__(self):
        return str(self.time)

    def GetTime(self):
        return str(self.time)
