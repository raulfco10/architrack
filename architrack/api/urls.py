from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("profile", views.ProfileViewSet, basename="profile")

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    #path('profile/', views.createProfile),
    path('locations/', views.createLocation),
    path('modalities/', views.createModality),
    path('skills/', views.createSkill),
    path('years/', views.createYear),

    url('', include(router.urls))
]