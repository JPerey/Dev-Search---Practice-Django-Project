from django.shortcuts import render
from django.http import HttpResponse

def projects(requests):
    return HttpResponse("here are our products")

def project(requests, pk):
    return HttpResponse("SINGLE PROJECT" + pk)