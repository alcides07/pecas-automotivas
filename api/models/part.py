from django.db import models

class Part(models.Model):
    part_number = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    details = models.TextField(max_length=555)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part_number} - {self.name}"

    class Meta:
        ordering = ['name']  