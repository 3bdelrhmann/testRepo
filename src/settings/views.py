from django.shortcuts import render
from django.http import HttpResponse

def privacy_and_terms(request):
    return HttpResponse('privacy_and_terms')
