from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),

    path('edit-account/', views.editAccount, name="edit-account"),
    path('edit-account-admin/<str:pk>/', views.editAccountByAdmin, name="edit-account-admin"),
    path('dro-form/<str:pk>/', views.droForm, name="dro-form"),
    path('commitment-form/<str:pk>/', views.commitmentForm, name="commitment-form"),
    path('checklist/<str:pk>/', views.checkList, name="checklist"),
    path('veracity-pdf/<str:pk>/', views.veracity_pdf, name="veracity-pdf"),
    path('commitment-pdf/<str:pk>/', views.commitment_pdf, name="commitment-pdf"),
    path('dro-pdf/<str:pk>/', views.dro_pdf, name="dro-pdf"),
    path('checklist-pdf/<str:pk>/', views.checklist_pdf, name="checklist-pdf"),



    path('create-skill/', views.createSkill, name="create-skill"),
    path('create-skill-admin/<str:pk>/', views.createSkillAdmin, name="create-skill-admin"),
    path('update-skill/<str:pk>/', views.updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.deleteSkill, name="delete-skill"),

    path('import-csv/', views.import_csv, name="import-csv"),

]