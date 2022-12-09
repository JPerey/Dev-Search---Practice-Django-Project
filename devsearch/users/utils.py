from django.db.models import Q
from .models import Skill, Profile


def searchProfiles(requests):
    search_text = ""

    if requests.GET.get("search_text"):
        search_text = requests.GET.get("search_text")
        print(search_text)

    skills = Skill.objects.filter(name__icontains=search_text)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_text) |
        Q(short_intro__icontains=search_text) |
        Q(skill__in=skills)
    )

    return profiles, search_text
