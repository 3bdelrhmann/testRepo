from django.core.validators import EmailValidator, validate_image_file_extension,RegexValidator
from authy.api import AuthyApiClient
from .models import User,LawyerDegrees,Country,Customer
from django.core.validators import RegexValidator
from django.conf import settings
from django import forms
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import datetime,timedelta
authy_api = AuthyApiClient(settings.TWILIO_PRODUCTION_KEY)

class RegisterUser(forms.ModelForm):
    GENDER_CHOICES = (
        ('ذكر', 'ذكر'),
        ('انثى', 'انثى'))

    first_name   = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'الأول',
    }),error_messages = {
            'required' : 'رجاءًا قم بكتابة أسمك'})
    last_name    = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'اسم العائلة \ اللقب',
    }),error_messages = {
            'required' : 'رجاءًا قم بكتابة اسم العائلة او اللقب'})
    email        = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'style' : 'direction:ltr',
    }),error_messages = {
            'invalid'  : 'البريد الإلكتروني غير صالح',
            'unique'   : 'مُستخدم اخر يستخدم هذا البريد الإلكتروني رجاءًا قم بتغييره',
            'required' : 'رجاءًا قم بكتابة البريد الإلكتروني الخاص بك'})
    password     = forms.CharField(min_length=8,max_length=255,required=True,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder':'•••••••••••••',
    }),error_messages = {
            'invalid'    : 'البريد الإلكتروني غير صالح',
            'min_length' : 'يجب ان تكون كلمة السر على الأقل مكونة من 8 أحرف',
            'required'   : 'رجاءًا قم بكتابة كلمة السر الخاصة بك'})
    phone_number = forms.CharField(max_length=13,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'01234567890',
    }),error_messages = {
            'required'   : 'رجاءًا قم بكتابة رقم الهاتف الخاص بك'})
    gender       = forms.ChoiceField(choices=GENDER_CHOICES,required=True,widget=forms.Select(attrs={
        'class' : 'form-control',
    }))
    birth_date   = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id'    : 'birthdate',
        'autocomplete' : 'off',
    }),error_messages = {
            'invalid'   : 'يجب ان يكون التاريخ بهذا التنسيق : yyyy-mm-dd',
            'required'   : 'رجاءًا أدخل تاريخ ميلادك'})
    profile_img  = forms.ImageField(max_length=100,required=False,widget=forms.FileInput(attrs={
        'class' : 'form-control custom-file-input',
        'id'    : 'imgFile',
        'autocomplete' : 'off',
        'accept': 'image/*'
    }),validators=[validate_image_file_extension])
    graduate_date = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id'    : 'graduate_date',
        'autocomplete' : 'off',
    }),error_messages = {
            'required'   : 'رجاءًا أدخل عام التخرج'})
    country       = forms.ModelChoiceField(queryset=Country.objects.all(),required=True,widget=forms.Select(attrs={
        'class' : 'form-control',
        'id'    : 'country',
    }),error_messages = {
            'required'   : 'رجاءًا إختر الدولة'})
    lawyer_degree = forms.ModelChoiceField(queryset=LawyerDegrees.objects.all(),required=True,widget=forms.Select(attrs={
        'class' : 'form-control',
    }),error_messages = {
            'required'   : 'رجاءًا إختر درجة قيدك بالنقابة'})
    office_add = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'3 ش , متفرع , الشارع الرئيسي',
        'id' : 'office_address',
    }),error_messages = {
            'required'   : 'رجاءًا قم بكتابة عنوان المكتب'})

    class Meta:
        model = User
        fields = ['first_name',
            'last_name',
            'email',
            'password',
            'phone_number',
            'gender',
            'birth_date',
            'profile_img',
            'lawyer_degree',
            'graduate_date',
            'country',
            'office_add']
            
    def clean_birth_date(self):
        birthdate = self.cleaned_data['birth_date']
        if datetime.strptime(birthdate,"%Y-%m-%d").year > (timezone.now() - relativedelta(years=23)).date().year:
            raise forms.ValidationError("عذرًا عُمرك أقل من العمر المسموح له بالتسجيل")
        return self.cleaned_data['birth_date']

class LoginForm(forms.Form):
    email    = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control form-control-sm email-login',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control form-control-sm password-login',
    }))
    class Meta:
        fields  = ['email','password']

class ReviewPhoneNumber(forms.ModelForm):
    class Meta:
        model   = User
        fields  = ['phone_number']
        widgets = {
            'phone_number' : forms.TextInput(attrs={
                'class' : 'form-control text-left',
                'style' : 'direction:ltr;',
            })}
class TokenVerificationForm(forms.Form):
    token = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'رمز الأمان',
        'autocomplete': 'off'
    }))

    def is_valid(self, authy_id):
        self.authy_id = authy_id
        return super(TokenVerificationForm, self).is_valid()

    def clean(self):
        token = self.cleaned_data['token']
        verification = authy_api.tokens.verify(self.authy_id, token)
        if not verification.ok():
            self.add_error('token', 'Invalid token')


class CreateCustomer(forms.ModelForm):
    mobile_number = forms.CharField(max_length=11,
    validators=[RegexValidator(regex='^[0][1][2?0?5?1]\d{8}$',message='رقم الهاتف غير صحيح')],
    error_messages={
        'required'   : 'رجاءًا ادخل رقم الهاتف الخاص بك',
        'max_length' : 'رقم الهاتف غير صحيح'
    })
    class Meta:
        model   = Customer
        fields  = ('name','mobile_number')
        error_messages = {
            'name' : {
                'required' : 'رجاءًا ادخل اسمك'
            }
        }