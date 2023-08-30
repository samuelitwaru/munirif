# serializers.py
from rest_framework import serializers
from .models import Department, Faculty, Proposal, Qualification, Profile, File, Score




class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
    
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

class ProposalSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, source='file_set')
    class Meta:
        model = Proposal
        fields = '__all__'

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
    faculty = FacultySerializer()
    department = DepartmentSerializer()
    qualification = QualificationSerializer()
    class Meta:
        model = Profile
        fields = '__all__'