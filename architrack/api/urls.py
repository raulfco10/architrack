from django.urls import path
from django.conf.urls import include
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("profile", views.ProfileViewSet, basename="profile")
router.register("course", views.CourseViewSet, basename="course")
router.register("skill", views.SkillViewSet, basename="skill")

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
    path('letters/', views.postLetterRegister, name="letter_history"),
    path('documentsupdate/', views.documentsUpdate),

    path('profile/', views.createProfile),
    path('locations/', views.createLocation),
    path('modalities/', views.createModality),
    #path('skills/', views.createSkill),
    path('years/', views.createYear),

    path('', include(router.urls))

]