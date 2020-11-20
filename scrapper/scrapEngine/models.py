from django.db import models

class Search(models.Model):
    recent_search = models.CharField(max_length=50)

    def __str__(self):
        return self.recent_search
