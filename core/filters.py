from rest_framework import filters
from django.contrib.auth.models import User
from .models import Score, Proposal

class ProposalFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Implement your custom filtering logic here
        # Modify the queryset as needed based on the request
        # For example:
        team__has = request.query_params.get('team__has')
        try:
            team__has = int(team__has)
        except:
            pass
        exclude__status = request.query_params.get('exclude__status')
        
        if team__has and isinstance(team__has, int):
            queryset = queryset.filter(team__user_id=team__has)
        if exclude__status and isinstance(exclude__status, str):
            queryset = queryset.exclude(status=exclude__status)
        
        return queryset
    
# class ProposalFilter(filters.FilterSet):
#     exclude_field_name = filters.CharFilter(method='filter_exclude_field_name')

#     class Meta:
#         model = Proposal
#         fields = {
#             'field_name': ['exact', 'icontains'],
#         }

#     def filter_exclude_field_name(self, queryset, name, value):
#         return queryset.exclude(**{name.replace('exclude_', ''): value})

class ScoreFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status__includes')
        if status: 
            status_list = status.split('|')
            return queryset.filter(status__in=status_list)
        return queryset

