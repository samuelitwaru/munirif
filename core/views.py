# views.py
from rest_framework import viewsets, filters
from accounts.serializers import UserSerializer

from utils.mails import send_html_email
from .models import Faculty, Proposal, Qualification, File, Score, Section
from .serializers import FacultySerializer, FileSerializer, ProposalSerializer, ProposalTeamSerializer, QualificationSerializer, ScoreSerializer, SectionSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


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
    
    @action(detail=True, methods=['GET'], name='team', url_path=r'team')
    def team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        team_srializer = UserSerializer(proposal.team, many=True)
        return Response(team_srializer.data)
    
    @action(detail=True, methods=['POST'], name='add_team', url_path=r'team/add', serializer_class=ProposalTeamSerializer)
    def add_team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        serializer = ProposalTeamSerializer(data=request.data)
        if proposal:
            bad_res_data = {'detail': 'Invalid Data'}
            if serializer.is_valid():
                data = request.data
                email = data.get('email')
                user = User.objects.get(username=email)
                user.groups.add(Group.objects.get(name='member'))
                token, _ = Token.objects.get_or_create(user=user)
                context = {'proposal': proposal, 'token':token, 'client_address': settings.CLIENT_ADDRESS}
                template = 'emails/member-invitation.html'
                if not user.is_active or not user.profile: template = 'emails/new-user-member-invitation.html'
                # if not user.is_active: template = 'emails/another.html'
                proposal.team.add(user)
                # send reviewership email
                # send_html_email(
                #     request,
                #     'PROPOSAL MEMBER INVITATION',
                #     [email],
                #     template,
                #     context
                # )
                team_srializer = UserSerializer(proposal.team, many=True)
                return Response(team_srializer.data)
            bad_res_data = serializer.errors
        return Response(bad_res_data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], name='remove_team', url_path=r'team/remove')
    def remove_team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        print(request.data)
        if proposal:
            data = request.data
            user_id = data['user']
            user = User.objects.get(id=user_id)
            if user:
                proposal.team.remove(user)
                team_srializer = UserSerializer(proposal.team, many=True)
                return Response(team_srializer.data)
        return Response({'detail': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        

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