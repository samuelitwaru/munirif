from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
import os
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver


STATUS_CHOICES = [
    ('EDITING', 'EDITING'),
    ('SUBMITTED', 'SUBMITTED'),
    ('SCORING', 'SCORING'),
    ('REVIEWED', 'REVIEWED'),
]

SCORE_STATUS_CHOICES = [
    ('PENDING', 'PENDING'),
    ('IN PROGRESS', 'IN PROGRESS'),
    ('COMPLETED', 'COMPLETED'),
]


from django.core.files.storage import FileSystemStorage

file_storage = FileSystemStorage(
    location=settings.PROPOSAL_FILES_DIR,
    base_url=settings.PROPOSAL_FILES_URL
)

class Section(models.Model):
     ref = models.CharField(max_length=16)
     name = models.CharField(max_length=32)
     title = models.CharField(max_length=32)

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
    status = models.CharField(max_length=64, default='EDITING', choices=STATUS_CHOICES) # editing, submitted, scoring, reviewed
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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

    problem_comment = models.TextField(null=True, blank=True)
    solution_comment = models.TextField(null=True, blank=True)
    outputs_comment = models.TextField(null=True, blank=True)
    team_comment  = models.TextField(null=True, blank=True)
    
    capacity_development_comment = models.TextField(null=True, blank=True)
    scalability_comment = models.TextField(null=True, blank=True)
    ethical_implications_comment = models.TextField(null=True, blank=True)
    conflict_of_interest_comment = models.TextField(null=True, blank=True)
    summary_budget_comment = models.TextField(null=True, blank=True)
    detailed_budget_comment = models.TextField(null=True, blank=True)
    workplan_comment = models.TextField(null=True, blank=True)

    strengths = models.TextField(null=True, blank=True)
    weaknesses = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True)

    status = models.CharField(max_length=64, default='PENDING', choices=SCORE_STATUS_CHOICES) # PENDING, ACCEPTED, COMPLETED
    user = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'proposal')
    
class File(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True, blank=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    file = models.FileField(storage=file_storage)


class Qualification(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name='profile')
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    qualification = models.ForeignKey(Qualification, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=8)
    phone = models.CharField(max_length=10)
    designation = models.CharField(max_length=32)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

@receiver(post_save, sender=Score)
@receiver(post_delete, sender=Score)
def on_score_status_change(sender, instance, **kwargs):
    proposal = instance.proposal
    scores = proposal.score_set.all()
    if all(list(map(lambda x: x.status=='COMPLETED', scores))):
        proposal.status = 'REVIEWED'
    else:
        proposal.status = 'SCORING'
    proposal.save()


@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    # Get the path to the file
    file_path = instance.file.path
    # Check if the file exists and delete it
    if os.path.isfile(file_path):
        os.remove(file_path)