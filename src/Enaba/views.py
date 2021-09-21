from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        return redirect('office:office_home')
    else:
        return render(request,'home.html')

def search_results(request):
    if request.user.is_authenticated:
        return redirect('office:office_home')
    else:
        return render(request,'search_results.html')