from django.db.models import Q
from .models import Skill, Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(requests, profiles, results):

    page = requests.GET.get("page")
    results = 3
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = Paginator.num_pages
        profiles = paginator.page(page)

    left_index = int(page) - 4
    right_index = int(page) + 5
    if left_index < 1:
        left_index = 1

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, profiles


def searchProfiles(requests):
    search_text = ""

    if requests.GET.get("search_text"):
        search_text = requests.GET.get("search_text")
        print(search_text)

    skills = Skill.objects.filter(name__icontains=search_text)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_text)
        | Q(short_intro__icontains=search_text)
        | Q(skill__in=skills)
    )

    return profiles, search_text
