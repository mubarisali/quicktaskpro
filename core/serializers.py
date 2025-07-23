from rest_framework import serializers
from .models import Organization, User, Project, Task
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'role', 'organization','password']
        extra_Kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
                                