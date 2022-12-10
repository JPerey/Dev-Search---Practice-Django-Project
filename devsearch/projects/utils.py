from django.db.models import Q
from .models import Tag, Project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(requests, projects, results):

    page = requests.GET.get("page")
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = Paginator.num_pages
        projects = paginator.page(page)

    left_index = int(page) - 4
    right_index = int(page) + 5
    if left_index < 1:
        left_index = 1

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, projects


def searchProjects(requests):
    search_text = ""

    if requests.GET.get("search_text"):
        search_text = requests.GET.get("search_text")

    tags = Tag.objects.filter(name__icontains=search_text)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_text)
        | Q(description__icontains=search_text)
        | Q(owner__name__icontains=search_text)
        | Q(tags__in=tags)
    )

    return projects, search_text
