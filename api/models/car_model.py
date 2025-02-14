from django.db import models
from api.models.part import Part

class CarModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    parts = models.ManyToManyField(Part, related_name="car_models", blank=True)

    def __str__(self):
        return f"{self.name} - {self.manufacturer} ({self.year})"

    class Meta:
        ordering = ['name']  
    