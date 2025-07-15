from django.db import models

class Franchise(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.location}"
