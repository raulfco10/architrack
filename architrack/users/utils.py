from logging import exception
import re
from .models import DroRegister, Modality, Profile, Skill, Location, LettersHistory
from django.db.models import Q
from django.contrib import messages

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        )

    return profiles, search_query

def sendDataDRO(request, pk):
    profile = Profile.objects.get(id=pk)
    location_field = request.GET.get('location')
    modality_field = request.GET.get('modality')
    registro = request.GET.get('registro')
    location = Location.objects.get(name = location_field)
    modality = Modality.objects.get(name = modality_field)
    type_of_letter = "dro"
    registro = request.GET.get('registro')

    print(request)
    try:
        letter = LettersHistory(
            owner = profile,
            letterType = type_of_letter,
            location = location,
            modality = modality,
            register = registro
        )
        letter.save()
        
        register, created = DroRegister.objects.get_or_create(
            owner = profile,
            location = location,
            modality = modality,
            register = registro
        )
        register.save()
    except exception:
        messages.error(request, 'Error la guardar historial o registro')


    return profile, location, modality.name, registro