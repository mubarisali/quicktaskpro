from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Organization, User, Project, Task
from .serializers import (
    OrganizationSerializer,
    UserSerializer,
    ProjectSerializer,
    TaskSerializer,
    CustomTokenObtainPairSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'assigned_to', 'due_date']

    def get_queryset(self):
        return Task.objects.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            organization=self.request.user.organization
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        org_name = self.request.data.get("organization")
        organization, created = Organization.objects.get_or_create(name=org_name)
        password = self.request.data.get("password")
        serializer.save(
            organization=organization,
            password=make_password(password),  # ✅ Hash password
            role='member'
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
