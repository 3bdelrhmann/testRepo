from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import twofa_required


def lawyer_session(request):
    
    template_name = 'phSessions/lawyerPhSession_request.html'
    context = {
        'title' : 'لديك إستشارة هاتفية جديدة',
    }
    return render(request,template_name,context)
    return HttpResponse('Lawyer Session')

def customer_session(request):
    return HttpResponse('Lawyer Session')