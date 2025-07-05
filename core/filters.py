from rest_framework import filters
from django.contrib.auth.models import User
from .models import Score, Proposal
from datetime import datetime

class ProposalFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Implement your custom filtering logic here
        # Modify the queryset as needed based on the request
        # For example:
        search_query = request.query_params.get('search_query')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        submission_date_lte = request.query_params.get('submission_date__lte')
        submission_date_gte = request.query_params.get('submission_date__gte')
        print(f"submission_date_lte: {submission_date_lte}, submission_date_gte: {submission_date_gte}")
        if submission_date_lte:
            date = datetime.strptime(submission_date_lte, "%Y/%m/%d").date()
            queryset = queryset.filter(submission_date__lte=date)
        if submission_date_gte:
            date = datetime.strptime(submission_date_gte, "%Y/%m/%d").date()
            queryset = queryset.filter(submission_date__gte=date)
        

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

