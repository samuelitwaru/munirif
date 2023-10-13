from rest_framework import filters

from django.contrib.auth.models import User

class ProposalFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Implement your custom filtering logic here
        # Modify the queryset as needed based on the request
        # For example:
        team__has = request.query_params.get('team_has')
        
        if team__has and isinstance(team__has, int):
            queryset = queryset.filter(team__user_id=team__has)
        return queryset

