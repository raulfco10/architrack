from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProfileSerializer, ProjectSerializer
from projects.models import Project, Review
from users.models import Profile

from api import serializers

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},
        {'POST':'api/profile'},

        {'POST':'api/users/token'},
        {'POST':'api/users/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProjects(request):
    #print('USER: ', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user, 
        project=project,
        )

    review.value = data['value']
    review.save()
    project.getVoteCount

    print('DATA: ', data)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProfile(request):
    user = request.user.profile
    data = request.data

    profile = Profile(
        user=data.user,
        agremiado_number = data.agremiado_number,
        name = data.name,
        email = data.email,
        username = data.username,
        phone = data.phone,
        mobile = data.mobile,
        degree_card_number = data.degree_card_number,
        request = data.request,
        veracity_letter = data.veracity_letter,
        degree = data.degree,
        photo = data.photo,
        inscription = data.inscription,
        annuity = data.annuity,
        degree_card = data.degree_card,
        speciallity_card = data.speciallity_card,
        rfc = data.rfc,
        proof_of_address = data.proof_of_address,
        ife = data.ife,
        curp = data.curp,
        resume = data.resume,
        sat_enrollment = data.sat_enrollment,
        thesis = data.thesis,
        referral_cards = data.referral_cards,
        born_certificate = data.born_certificate,
        municipality_licence = data.municipality_licence,
        state_card = data.state_card
    )

    profile.save()

    serializer = ProjectSerializer(profile, many=False)
    return Response(serializer.data)