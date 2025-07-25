from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet, 
    UserViewSet, 
    ProjectViewSet, 
    TaskViewSet, 
    RegisterView,
    CustomTokenObtainPairView  # ✅ Import custom view
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('users', UserViewSet)
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Email-based login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
