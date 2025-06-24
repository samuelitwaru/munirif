from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import GroupViewSet, UserViewSet
from .views import *
from munirif import router

# Create a router and register our viewset with it.
router.register(r'calls', CallViewSet)
router.register(r'reporting-dates', ReportingDateViewSet)
router.register(r'themes', ThemeViewSet)
router.register(r'profile-themes', ProfileThemeViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'files', FileViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'scores', ScoreViewSet)
# router.register(r'users', UserViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'qualifications', QualificationViewSet)
router.register(r'entities', EntityViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]