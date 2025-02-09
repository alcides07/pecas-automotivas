from django_filters import rest_framework as filters
from ..models import Part

class PartFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price_gte = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_lte = filters.NumberFilter(field_name="price", lookup_expr='lte')


    class Meta:
        model = Part
        fields = ['part_number']
