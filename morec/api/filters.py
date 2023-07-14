from django_filters import rest_framework as filters
from movies.models import Movie


class MoviesFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    orig_title = filters.CharFilter(field_name='original_title', lookup_expr='icontains')
    actor = filters.CharFilter(field_name='actors', lookup_expr='name__icontains')
    director = filters.CharFilter(field_name='directors', lookup_expr='name__icontains')
    genre = filters.CharFilter(field_name='genres', lookup_expr='slug__exact')
    category = filters.CharFilter(field_name='categories', lookup_expr='slug__exact')
    country = filters.CharFilter(field_name='countries', lookup_expr='slug__exact')
    year = filters.NumberFilter(field_name='premiere_date', lookup_expr='year__exact')
    year_gt = filters.NumberFilter(field_name='premiere_date', lookup_expr='year__gte')
    year_lt = filters.NumberFilter(field_name='premiere_date', lookup_expr='year__lte')

    class Meta:
        model = Movie
        fields = ('title',)
