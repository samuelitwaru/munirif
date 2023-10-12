# views.py
from rest_framework import viewsets, filters

from utils.mails import send_html_email
from .models import Faculty, Proposal, Qualification, File, Score, Section
from .serializers import FacultySerializer, FileSerializer, ProposalSerializer, QualificationSerializer, ScoreSerializer, SectionSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework.authtoken.models import Token


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    search_fields = ['title']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params.dict()
        if 'search' in params:
            params.pop('search')
        if params:
            queryset = queryset.filter(**params)
        return queryset


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.data['user']
        email = request.data['email']
        proposal = request.data['proposal']
        proposal = Proposal.objects.get(id=proposal)
        user, created = User.objects.get_or_create(username=email)
        user.groups.add(Group.objects.get(name='reviewer'))
        request.data['user'] = user.id
        token, _ = Token.objects.get_or_create(user=user)
        context = {'proposal': proposal, 'token':token, 'client_address': settings.CLIENT_ADDRESS}
        template = 'emails/review-invitation.html'
        if not user.is_active or not user.profile: template = 'emails/new-user-review-invitation.html'
        # if not user.is_active: template = 'emails/another.html'
        print('>>>>>>>>>>', template)
        if created:
            user.is_active = False
            user.save()

        # send reviewership email
        send_html_email(
            request,
            'PROPOSAL REVIEW INVITATION',
            [email],
            template,
            context
        )
        return super().create(request, *args, **kwargs)

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer