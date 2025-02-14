from django_filters import rest_framework as filters
from ..models import CarModel

class CarModelFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    manufacturer = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter(field_name="year", lookup_expr='exact')
    year_gte = filters.NumberFilter(field_name="year", lookup_expr='gte')
    year_lte = filters.NumberFilter(field_name="year", lookup_expr='lte')

    class Meta:
        model = CarModel
        fields = ['year']
