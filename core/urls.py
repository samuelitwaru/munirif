from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import GroupViewSet, UserViewSet
from .views import FacultyViewSet, FileViewSet, ProposalViewSet, QualificationViewSet, ScoreViewSet, SectionViewSet
from munirif import router

# Create a router and register our viewset with it.
router.register(r'sections', SectionViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'files', FileViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'users', UserViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'qualifications', QualificationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]