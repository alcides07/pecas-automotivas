from django.contrib import admin
from api.models import CarModel


class CarModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(CarModel, CarModelAdmin)
