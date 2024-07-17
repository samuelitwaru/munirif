# custom_filters.py
from rest_framework import filters

import django_filters
from django.contrib.auth.models import User
from core.models import ProfileTheme


class UserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Implement your custom filtering logic here
        # Modify the queryset as needed based on the request
        # For example:
        group_names = request.query_params.get('groups__name__in')
        theme_ids = request.query_params.get('themes__in')
        if group_names and isinstance(group_names, str):
            group_names = group_names.split(',')
            queryset = queryset.filter(groups__name__in=group_names)
        if theme_ids and isinstance(theme_ids, str):
            theme_ids = theme_ids.split(',')
            profiles = ProfileTheme.objects.filter(theme__in=theme_ids).values_list('profile', flat=True)
            queryset = queryset.filter(profile__in=profiles)
        return queryset




