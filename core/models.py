from django.db import models
# Create your models here.


class Proposal(models.Model):
    subject = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    problem = models.CharField(max_length=5000)
    solution = models.CharField(max_length=5000)
    budget = models.CharField(max_length=5000)
    
    
class File(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)


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
    