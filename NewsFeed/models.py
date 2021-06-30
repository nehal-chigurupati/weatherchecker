from django.db import models
from django.conf import settings

class LocationCoordinates(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    coordinates = models.CharField(max_length=100, default="UNAVAILABLE")

    def GetCoordinates(self):
        return str(self.coordinates)

    def __str__(self):
        return str(self.time)

    def GetTime(self):
        return str(self.time)

class WikiPage(models.Model):
    search_term = models.CharField(max_length=255, blank=False, null=False)
    added_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return str(self.search_term)

    def get_search_term(self):
        return str(self.search_term)

    def get_full_text(self):
        return str(self.text)


    class Meta:
        managed=False
        db_table='newsfeed_wikipage'
        #db_table = 'NewsFeed_wikipage'
