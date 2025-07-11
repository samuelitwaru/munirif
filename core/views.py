# views.py
import threading
import openpyxl
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from accounts.serializers import UserSerializer
from core.filters import ProposalFilter, ScoreFilter
# from core.tasks import delete_expired_invitations
from core.utils import generate_excel_from_schema
from utils.helpers import get_host_name, write_proposal_pdf, write_xlsx_file
from datetime import datetime, timedelta
from django.utils import timezone
from utils.mails import send_html_email
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.order_by('-submission_date').all()
    serializer_class = ProposalSerializer
    search_fields = ['title']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, ProposalFilter]
    filterset_fields = '__all__'
   
    @action(detail=False, methods=['GET'], name='count', url_path=r'count')
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        return Response({'count': count})
    
    @action(detail=True, methods=['GET'], name='team', url_path=r'team')
    def team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        team_srializer = UserSerializer(proposal.team_members, many=True)
        return Response(team_srializer.data)
    
    @action(detail=True, methods=['POST'], name='add_team', url_path=r'team/add', serializer_class=ProposalTeamSerializer)
    def add_team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        serializer = ProposalTeamSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.error_messages)
        if proposal:
            bad_res_data = {'detail': 'Invalid Data'}
            if serializer.is_valid():
                data = request.data
                email = data.get('email')
                user = User.objects.get(username=email)
                proposal.team_members.add(user)
                team_srializer = UserSerializer(proposal.team_members, many=True)
                return Response(team_srializer.data)
            bad_res_data = serializer.errors
        return Response(bad_res_data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], name='remove_team', url_path=r'team/remove')
    def remove_team(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        if proposal:
            data = request.data
            user_id = data['user']
            user = User.objects.get(id=user_id)
            if user:
                proposal.team_members.remove(user)
                team_srializer = UserSerializer(proposal.team_members, many=True)
                return Response(team_srializer.data)
        return Response({'detail': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='download_score_sheet', url_path=r'score-sheet/download')
    def download_score_sheet(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        sections = Section.objects.all()
        scores = proposal.score_set.all()
        rows = []
        for index, section in enumerate(sections):
            data = [section.title] + [getattr(score, section.name) for score in scores] + [f"=sum({chr(ord('b'))}{index+2}:{chr(ord('b')+len(scores)-1)}{index+2})"] + [f"=average({chr(ord('b'))}{index+2}:{chr(ord('b')+len(scores)-1)}{index+2})"]
            rows.append(data)
        columns = ['Section'] + [str(score.user) for score in scores] + ['TOTAL', 'AVERAGE']

        foot = ['TOTAL'] + [f'=sum({chr(num)}2:{chr(num)}12)' for num in range(ord('b'), ord('b')+len(scores))]
        rows.append(foot)
        file = write_xlsx_file(f'score-sheet-{proposal.id}.xlsx', columns, rows)
        host = get_host_name(request)
        return Response({'file_url':f'{host}{file}'}) 
    
    @action(detail=True, methods=['GET'], name='download_pdf', url_path=r'pdf/download')
    def download_pdf(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(id=pk)
        file = write_proposal_pdf(f'{proposal.title}.pdf', proposal)
        host = get_host_name(request)
        return Response({'file_url':f'{host}{file}'}) 
    
    @action(detail=False, methods=['GET'], name='download_bulk_upload_sheet', url_path=r'bulk-upload-sheet/download')
    def download_bulk_upload_sheet(self, request, *args, **kwargs):
        schema =  [
            {
                "name": "Title",
                "validation": {"type": "textLength", "operator": "lessThanOrEqual", "formula1": 15},
            },
            {
                "name": "Theme",
                "validation": {"type": "list", "formula1": f'"{",".join([theme.title for theme in Theme.objects.all()])}"', "allow_blank": False},
            },
            {
                "name": "Status",
                "validation": {"type": "list", "formula1": '"PENDING,SELECTED"', "allow_blank": False},
            },
            {
                "name": "PI",
                "validation": {"type": "list", "formula1": f'"{",".join([user.username for user in User.objects.filter(groups__name="reviewer")])}"', "allow_blank": False},
            },
            {
                "name": "Call",
                "validation": {"type": "list", "formula1": f'"{",".join([call.title for call in Call.objects.all()])}"', "allow_blank": True},
            }
        ]
        file = generate_excel_from_schema(schema)
        host = get_host_name(request)
        return Response({'file_url':f'{host}{file}'})
    
    @action(detail=False, methods=['POST'], name='upload_bulk', url_path=r'upload-bulk')
    def upload_bulk(self, request, *args, **kwargs):
        print('request.data', request.data)
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            print(sheet.iter_rows(min_row=2, values_only=True))
            created = 0
            for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):  # skip header row
                print('>>>', row)
                # Assuming columns: First Name, Last Name, Email
                title, theme_title, p_status, pi_email, call_title = row
                if not title:
                    continue  # skip rows without required data
                
                call = Call.objects.filter(title=call_title).first()
                theme = Theme.objects.filter(title=theme_title).first()
                user = User.objects.filter(username=pi_email).first()


                # Save to database (adjust field names as needed)
                Proposal.objects.create(
                    title=title,
                    call=call,
                    user=user,
                    theme=theme,
                    status=p_status
                )
                created += 1

            return Response({"message": f"{created} records imported"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"


class ProfileThemeViewSet(viewsets.ModelViewSet):
    queryset = ProfileTheme.objects.all()
    serializer_class = ProfileThemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"
    

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    @action(detail=True, methods=['GET'], name='set_as_active', url_path=r'set-as-active')
    def set_as_active(self, request, pk, *args, **kwargs):
        call = get_object_or_404(Call, id=pk)
        call.is_active = True
        call.save()

        Call.objects.exclude(id=pk).update(is_active=False)

        entity = Entity.objects.first()
        if entity: 
            entity.current_call = call
            entity.save()
        data = CallSerializer(call).data
        return Response(data, status=status.HTTP_200_OK)


class ReportingDateViewSet(viewsets.ModelViewSet):
    queryset = ReportingDate.objects.all()
    serializer_class = ReportingDateSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['proposal_id', 'attachment_id']


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['proposal_id', 'reporting_date_id']

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    filter_backends = [DjangoFilterBackend, ScoreFilter]
    filterset_fields = ['proposal', 'status', 'user']
    
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
        # if not user.is_active: template = 'emails/another.html'
        if created:
            user.is_active = False
            user.save()

        template = 'emails/review-invitation.html'
        if not user.is_active or not user.profile: template = 'emails/new-user-review-invitation.html'
        
        threading.Thread(target=send_html_email, args=(
            request,
            'PROPOSAL REVIEW INVITATION',
            [email],
            template,
            context
        )).start()

        # send reviewership email
        # send_html_email(
        #     request,
        #     'PROPOSAL REVIEW INVITATION',
        #     [email],
        #     template,
        #     context
        # )
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['GET'], name='validate', url_path=r'validate')
    def validate(self, request, pk, *args, **kwargs):
        score = get_object_or_404(Score, id=pk)
        is_expired = timezone.now() > score.expires_at
        return Response({'is_expired': is_expired}, status=status.HTTP_200_OK)

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

