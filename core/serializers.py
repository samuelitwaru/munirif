# serializers.py
from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class ProposalSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, source='file_set', read_only=True)
    user__first_name = serializers.CharField(source='user.first_name', read_only=True)
    user__last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Proposal
        fields = '__all__'
        read_only_fields = ('team_members',)
        

class ProposalTeamSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ScoreSerializer(serializers.ModelSerializer):
    user__first_name = serializers.CharField(source='user.first_name', read_only=True)
    user__last_name = serializers.CharField(source='user.last_name', read_only=True)
    user__username = serializers.CharField(source='user.username', read_only=True)
    total_score = serializers.IntegerField(read_only=True)
    proposal_detail = ProposalSerializer(source='proposal', read_only=True)
    class Meta:
        model = Score
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, source='department_set')
    class Meta:
        model = Faculty
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'