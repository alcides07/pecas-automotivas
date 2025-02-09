from django.contrib import admin
from api.models import Part


class PartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Part, PartAdmin)
