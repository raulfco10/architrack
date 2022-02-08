from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProfileSerializer, ProjectSerializer, LocationSerializer, ModalitySerializer, SkillSerializer, YearSerializer
from projects.models import Project, Review
from users.models import Profile, Location, Modality, Skill, Year, Course

from api import serializers

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},
        {'POST':'api/profile'},
        {'POST':'api/locations'},
        {'POST':'api/modalities'},
        {'POST':'api/skills'},
        {'POST':'api/years'},

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

    #print('DATA: ', data)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProfile(request):
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

    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createLocation (request):
    data = request.data
    #print("BODY: ", data)

    location, created = Location.objects.get_or_create(
        name=data['name'], 
        responsible=data['responsible'],
        )

    location.description = data['description']
    location.address = data['address']
    location.save()

    serializer = LocationSerializer(location, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createModality (request):
    data = request.data
    #print("BODY: ", data)

    modality, created = Modality.objects.get_or_create(
        name=data['name'], 
        )
    modality.description = data['description']
    modality.save()

    serializer = ModalitySerializer(modality, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSkill (request):
    data = request.data
    #print("BODY: ", data)

    skill, created = Skill.objects.get_or_create(
        owner = data['owner'],
        name = data['name'], 
        )
    skill.description = data['description']
    skill.save()

    serializer = SkillSerializer(skill, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createYear (request):
    data = request.data
    #print("BODY: ", data)

    year, created = Year.objects.get_or_create(
        name = data['name'], 
        )
    year.save()

    serializer = YearSerializer(year, many=False)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    def get_queryset(self):
        profile = Profile.objects.all()
        return profile

    def create(self, request, *args, **kwargs):
        data = request.data

        new_profile = Profile(
            agremiado_number = data['agremiado_number'],
            name = data['name'],
            email = data['email'],
            username = data['username'],
            phone = data['phone'],
            mobile = data['mobile'],
            degree_card_number = data['degree_card_number'],
            request = data['request'],
            veracity_letter = data['veracity_letter'],
            degree = data['degree'],
            photo = data['photo'],
            inscription = data['inscription'],
            annuity = data['annuity'],
            degree_card = data['degree_card'],
            speciallity_card = data['speciallity_card'],
            rfc = data['rfc'],
            proof_of_address = data['proof_of_address'],
            ife = data['ife'],
            curp = data['curp'],
            resume = data['resume'],
            sat_enrollment = data['sat_enrollment'],
            thesis = data['thesis'],
            referral_cards = data['referral_cards'],
            born_certificate = data['born_certificate'],
            municipality_licence = data['municipality_licence'],
            state_card = data['state_card']
        )

        new_profile.save()

        for location in data['location']:
            location_obj = Location.objects.get(name=location["name"])
            new_profile.location.add(location_obj)

        for modality in data['modality']:
            modality_obj = Modality.objects.get(name=modality["name"])
            new_profile.modality.add(modality_obj)

        for year in data['years']:
            year_obj = Year.objects.get(name=year["name"])
            new_profile.years.add(year_obj)
        
        for course in data['courses']:
            course_obj = Course.objects.get(name=course["name"])
            new_profile.years.add(course_obj)

        serializer = ProfileSerializer(new_profile)
        return Response(serializer.data)

