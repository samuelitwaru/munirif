from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('EDITING', 'EDITING'),
    ('SUBMITTED', 'SUBMITTED'),
    ('SCORING', 'SCORING'),
]

class Proposal(models.Model):
    title = models.CharField(max_length=128)
    problem = models.TextField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    outputs = models.TextField(null=True, blank=True)
    team  = models.TextField(null=True, blank=True)
    capacity_development = models.TextField(null=True, blank=True)
    scalability = models.TextField(null=True, blank=True)
    ethical_implications = models.TextField(null=True, blank=True)
    conflict_of_interest = models.TextField(null=True, blank=True)
    summary_budget = models.TextField(null=True, blank=True)
    detailed_budget = models.TextField(null=True, blank=True)
    workplan = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=64, default='EDITING', choices=STATUS_CHOICES) # editing, submitted, scoring


class Score(models.Model):
    problem = models.IntegerField(null=True)
    solution = models.IntegerField(null=True)
    outputs = models.IntegerField(null=True)
    team  = models.IntegerField(null=True)
    
    capacity_development = models.IntegerField(null=True)
    scalability = models.IntegerField(null=True)
    ethical_implications = models.IntegerField(null=True)
    conflict_of_interest = models.IntegerField(null=True)
    summary_budget = models.IntegerField(null=True)
    detailed_budget = models.IntegerField(null=True)
    workplan = models.IntegerField(null=True)

    strengths = models.TextField(null=True)
    weaknesses = models.TextField(null=True)
    comment = models.TextField(null=True)


    user = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    
    
class File(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True, blank=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    file = models.FileField(upload_to=settings.PROPOSAL_FILES_DIR, max_length=100)


class Qualification(models.Model):
    name = models.CharField(max_length=64)

class Faculty(models.Model):
    name = models.CharField(max_length=64)


class Department(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name='profile')
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    qualification = models.ForeignKey(Qualification, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=8)
    phone = models.IntegerField()
    