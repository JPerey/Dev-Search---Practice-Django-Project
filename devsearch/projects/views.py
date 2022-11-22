from django.shortcuts import render
from django.http import HttpResponse

def projects(requests):
    return render(requests, 'projects.html')

def project(requests, pk):
    return render(requests, 'single-project.html')