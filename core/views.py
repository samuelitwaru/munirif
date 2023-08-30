# views.py
from rest_framework import viewsets, filters
from .models import Faculty, Proposal, Qualification, File, Score
from .serializers import FacultySerializer, FileSerializer, ProposalSerializer, QualificationSerializer, ScoreSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    search_fields = ['title']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # @action(detail=True, methods=['POST'], name='submit', url_path='submit')
    # def sumit(self, request, *args, **kwargs):
    #     data = request.data
    #     setup_levels(data)
    #     level_groups = super().get_queryset()
    #     serializer = self.get_serializer(level_groups, many=True)
    #     return Response(serializer.data)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def create(self, request, *args, **kwargs):
        user = request.data['user']
        email = request.data['email']
        if email and not user :
            user, created = User.objects.get_or_create(username=email, email=email, is_active=False)
            user.groups.add(Group.objects.get(name='reviewer'))
            # send reviewership email
            request.data['user'] = user.id
        return super().create(request, *args, **kwargs)

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer