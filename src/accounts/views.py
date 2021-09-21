from accounts.models import Country,Governorate,Region,VerifyLastSentIn
from .forms import TokenVerificationForm,ReviewPhoneNumber,RegisterUser,LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from rest_framework.response import Response
from .decorators import twofa_required
from authy.api import AuthyApiClient
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .models import User
import json

authy_api = AuthyApiClient(settings.TWILIO_PRODUCTION_KEY)

from dateutil.relativedelta import relativedelta

@twofa_required
def user_home(request):
    return redirect('accounts:login')

def reset_password(request):
    return HttpResponse('reset password')

def login(request):
    if request.user.is_authenticated:
        return redirect('office:office_home')
    Login_Form = LoginForm(request.POST or None)
    if Login_Form.is_valid():
        email = Login_Form.cleaned_data.get('email')
        password = Login_Form.cleaned_data.get('password')
        userLogCheck = authenticate(request, email=email, password=password)
        if userLogCheck is not None:
            auth_login(request, userLogCheck)        
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('office:office_home')
        else:
            messages.warning(
                request, 'كلمة المرور او البريد الإلكتروني أحدهم غير صحيح برجاء المحاولة مرة أخرة او يمكنك <b><a href="'+ redirect('accounts:reset_password').url +'">إستعادة كلمة المرور</a></b>',extra_tags='safe')
            return redirect('accounts:login')
    context = {
        'LoginForm' : Login_Form,
        'title' : 'تسجيل الدخول',
    }
    return render(request,'accounts/login.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('office:office_home')
    
    if request.method == 'POST':
        RegisterForm = RegisterUser(request.POST,request.FILES)
        if RegisterForm.is_valid():
            email    = request.POST.get('email')
            password = request.POST.get('password')
            _RegisterForm = RegisterForm.save(commit=False)
            _RegisterForm.set_password(RegisterForm.cleaned_data['password'])
            _RegisterForm.governorate_id = request.POST.get('governorate')
            _RegisterForm.region_id      = request.POST.get('region')
            _RegisterForm.save()
            userLogCheck = authenticate(request, email=email, password=password)
            if userLogCheck != None:
                auth_login(request, userLogCheck)
                return redirect('accounts:review')
    else:
        RegisterForm = RegisterUser()
    context = {
        'RegisterForm' : RegisterForm,
        'title' : 'التسجيل',
    }
    
    return render(request,'accounts/register.html',context)

#-login-required-
@login_required()
def review_phone(request):
    if request.method == 'POST':
        form = ReviewPhoneNumber(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            get_user = request.user
            if get_user.authy_id is None:
                authy_user = authy_api.users.create(
                                request.user.email,
                                request.user.phone_number,
                                request.user.country_code)
                get_user.authy_id = authy_user.id
            get_user.save()
            return redirect('accounts:verify')
    else:
        form = ReviewPhoneNumber(instance=request.user) 

    context = {
        'title' : 'مراجعة رقم الهاتف',
        "form" : form,
    }
    return render(request,'accounts/phone_review.html',context)


@login_required()
def verfiy_phone(request):
    if request.user.phone_verified:
        return redirect('office:office_home')
    if request.user.send_code:
        sms = authy_api.users.request_sms(request.user.authy_id, {'force': True})
        get_user = request.user
        get_user.send_code = False
        get_user.save()
        messages.add_message(request,messages.SUCCESS,message='تم إرسال الرمز إلي هاتفك في رسالة نصية')
    if request.method == 'POST':
        form = TokenVerificationForm(request.POST)
        if form.is_valid(request.user.authy_id):
            request.user.phone_verified = True
            request.user.send_code = False
            get_efforts = request.user.last_sent
            get_efforts.efforts = 0
            get_efforts.save()
            request.user.save()
            return redirect('accounts:verify')
        else:
            messages.add_message(request,messages.WARNING,message='الرمز اللذي أدخلته خاطئ')
    else:
        form = TokenVerificationForm()

    context = {
        'form' : form,
        'title' : 'التحقق من رقم الهاتف',
    }
    return render(request,'accounts/verify_phone.html',context)

def lawyer_profile(request,lawyer_id):
    try:
        get_lawyer = User.objects.prefetch_related('specialties').select_related('lawyer_degree','region','country','governorate').get(id=lawyer_id)
    except User.DoesNotExist:
        return HttpResponse('Not Found Choose another lawyer')
    if get_lawyer.is_banned        \
        or get_lawyer.is_banned     \
        or get_lawyer.in_review      \
        or get_lawyer.is_deleted      \
        or get_lawyer.is_assistant     \
        or get_lawyer.blocked_booking   \
        or not get_lawyer.phone_verified:
            return HttpResponse('Not Found Choose another lawyer')
    lawyer_available = True
    if not get_lawyer.onsite_book and not get_lawyer.phone_book:
        lawyer_available = False

    years_exprience = timezone.now().year - get_lawyer.graduate_date.year
    template_name = 'accounts/profile/profile.html'

    context = {
        'lawyer_info' : get_lawyer,
        'lawyer_available' : lawyer_available,
        'years_exprience' : years_exprience,
        'title' : 'المحامي',
    }
    return render(request,template_name,context)