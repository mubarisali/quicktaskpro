from rest_framework import viewsets, permissions
from .models import Organization, User, Project, Task
from .serializers import OrganizationSerializer, UserSerializer, ProjectSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'assigned_to', 'due_date']
    def get_queryset(self):
        return Task.objects.filter(organization=self.request.user.organization)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user, organization=self.request.user.organization)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)    
              