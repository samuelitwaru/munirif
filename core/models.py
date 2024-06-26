from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
import os
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone


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

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class Call(TimeStampedModel):
    title = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Section(models.Model):
     ref = models.CharField(max_length=128)
     name = models.CharField(max_length=128)
     title = models.CharField(max_length=128)
     word_limit = models.IntegerField(default=500)

class Proposal(TimeStampedModel):
    title = models.CharField(max_length=128)
    call = models.ForeignKey(Call, on_delete=models.SET_NULL, null=True)
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
    team_members = models.ManyToManyField(User, related_name='team_proposals')


class Score(TimeStampedModel):
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

    accepted_at = models.DateTimeField(null=True)
    is_recommended = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(7))
    
    class Meta:
        unique_together = ('user', 'proposal')
    
    def save(self, *args, **kwargs):
        expires_at = timezone.now() + timedelta(7)
        self.expires_at = expires_at
        super(Score, self).save(*args, **kwargs)
    
    @property
    def total_score(self):
        sections = map(lambda x: x.name, Section.objects.all())
        return sum([(getattr(self, section, 0) or 0) for section in sections])
    
class File(models.Model):
    name = models.CharField(max_length=128)
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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    # Get the path to the file
    file_path = instance.file.path
    # Check if the file exists and delete it
    if os.path.isfile(file_path):
        os.remove(file_path)