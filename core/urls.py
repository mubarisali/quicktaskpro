from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, UserViewSet, ProjectViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('users', UserViewSet)
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ TRAILING SLASH INCLUDED
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
