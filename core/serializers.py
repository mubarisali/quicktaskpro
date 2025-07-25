from rest_framework import serializers
from .models import Organization, User, Project, Task
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

UserModel = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'full_name', 'email', 'role', 'organization', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        org_name = validated_data.pop('organization')
        full_name = validated_data.pop('full_name')
        organization, _ = Organization.objects.get_or_create(name=org_name)
        user = UserModel.objects.create(
            username=full_name,
            email=validated_data.get('email'),
            password=make_password(validated_data.get('password')),
            organization=organization,
            role='member'
        )
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# Custom JWT Login Serializer using email
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate using email
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        return super().validate(attrs)
