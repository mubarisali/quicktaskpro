from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=100)
    
class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    ROLE_CHOICES = [('admin', 'Admin'), ('manager', 'Manager'), ('member', 'Member')]  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
class Task(models.Model):
    STATUS = [('todo', 'To Do'), ('inprogress', 'In Progress'), ('done', 'Done')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="tasks")
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)  
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')  
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_tasks')    

