from django.http import JsonResponse


def getRoutes(requests):

    routes = [
        {"GET": "api/projects"},
        {"GET": "api/projects/id"},
        {"POST": "api/projects/id/vote"},
        {"POST": "api/users/token"},
        {"POST": "api/users/token/refresh"},
    ]

    return JsonResponse(routes, safe=False)
