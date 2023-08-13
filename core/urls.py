from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet
from .views import FacultyViewSet, ProposalViewSet, QualificationViewSet
from munirif import router

# Create a router and register our viewset with it.
router.register(r'users', UserViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'users', UserViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'qualifications', QualificationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]