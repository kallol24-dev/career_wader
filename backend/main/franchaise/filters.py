import django_filters
from franchaise.models import Franchise

class FilterClassFranchise(django_filters.FilterSet):
    state = django_filters.CharFilter(field_name='user__state', lookup_expr='exact')
    city = django_filters.CharFilter(field_name='user__city', lookup_expr='exact')
    country = django_filters.CharFilter(field_name='user__country', lookup_expr='exact')
    created_at = django_filters.DateFilter(field_name='user__created_at', lookup_expr='exact')

    class Meta:
        model = Franchise
        fields = ['state', 'city', 'country', 'created_at']