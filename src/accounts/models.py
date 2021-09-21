from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from django.core.validators import RegexValidator,validate_image_file_extension
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from uuid import uuid4
from time import time

def user_folder_direction(instance, filename, **kwargs):
    title = str(time()).replace('.', '_')
    file_path = f'profiles/{instance.email}/{title}-{filename}'
    return file_path

def validate_birthdate(birthdate):
    if birthdate.year > (timezone.now() - relativedelta(years=23)).date().year  :
        return ValidationError(('You shod bigger than  %(birthdate)s'),
            params={'birthdate': birthdate},
            code='min_birthdate',)

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_banned', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Specialties(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField("الدولة",max_length=250,)
    slug = models.SlugField("الإسم المختصر",allow_unicode=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "countries"
        verbose_name_plural = "countries"

class Governorate(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    name = models.CharField("المحافظة",max_length=250,)
    slug = models.SlugField("الإسم المختصر",allow_unicode=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "governorates"
        verbose_name_plural = "governorates"

class Region(models.Model):
    governorate = models.ForeignKey(Governorate,on_delete=models.CASCADE)
    name = models.CharField("المنطقة",max_length=250,)
    slug = models.SlugField("الإسم المختصر",allow_unicode=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "regions"
        verbose_name_plural = "regions"

class LawyerDegrees(models.Model):
    name = models.CharField("درجة القيد",max_length=250,)
    slug = models.SlugField("الإسم المختصر",allow_unicode=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Lawyer Degree"
        verbose_name_plural = "Lawyer Degrees"

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('ذكر', 'ذكر'),
        ('انثى', 'انثى')
    )
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.UUIDField(default=uuid4)
    register_date = models.DateTimeField(auto_now_add=True,editable=False)
    country_code  = models.CharField(max_length=6,verbose_name="كود الدولة",default='+20')
    phone_number  = models.CharField(max_length=13,null=True ,unique=True,validators=[RegexValidator(regex='^[0][1][2?0?5?1]\d{8}$',message='رقم الهاتف غير صحيح')])
    first_name    = models.CharField(blank=True,null=True,max_length=100,verbose_name="الاسم الاول")
    last_name     = models.CharField(blank=True,null=True,max_length=100,verbose_name="اسم العائلة")
    profile_img   = models.ImageField(default='default.png',verbose_name="الصورة الشخصية",upload_to=user_folder_direction, null=True,validators=[validate_image_file_extension])
    graduate_date = models.DateField(blank=True,null=True,verbose_name='عام التخرج')
    birth_date  = models.DateField(blank=True,null=True,verbose_name='تاريخ الميلاد')
    gender      = models.CharField(blank=True,null=True,verbose_name='الجنس',max_length=20, choices=GENDER_CHOICES)
    country     = models.ForeignKey(Country,blank=True,verbose_name='الدولة',on_delete=models.SET_NULL,null=True)
    governorate = models.ForeignKey(Governorate,blank=True,verbose_name='المحافظة',on_delete=models.SET_NULL,null=True)
    region      = models.ForeignKey(Region,blank=True,verbose_name='المقاطعة / المنطقة',on_delete=models.SET_NULL,null=True)
    specialties = models.ManyToManyField(Specialties,verbose_name='التخصصات',max_length=500,blank=True,related_name='all_specialties')
    about       = models.TextField(verbose_name='عن المحامي',max_length=500,blank=True,null=True)
    office_add  = models.CharField(verbose_name='عنوان المكتب',max_length=250,blank=True,null=True)
    lawyer_degree   = models.ForeignKey(LawyerDegrees,blank=True,verbose_name='درجة القيد',on_delete=models.SET_NULL,null=True)
    authy_id    = models.CharField(max_length=20, null=True, blank=True)
    wallet      = models.FloatField(default=0,blank=True,null=True,verbose_name='المحفظة')
    blocked_booking = models.BooleanField(default=False)
    phone_verified  = models.BooleanField(default=False)
    send_code = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    in_review = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    onsite_book = models.BooleanField(default=False)
    phone_book  = models.BooleanField(default=False)
    
    onsite_cost = models.FloatField(default=100)
    phone_cost  = models.FloatField(default=100)

    allow_reset_password = models.BooleanField(default=True)
    is_deleted  = models.BooleanField(default=False)

    #-----------Assistant Attrs-----------#
    is_assistant    = models.BooleanField(default=False)
    assistant_to    = models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,related_name='lawyer_assistants')
    allow_assistant_update = models.BooleanField(default=False)
    allow_assistant_delete = models.BooleanField(default=False)
    allow_assistant_add    = models.BooleanField(default=False)
    data_is_restricted     = models.BooleanField(default=False) # data is restricted to show the only data who's assigned to him only not all data of the main office

    USERNAME_FIELD  = 'email'
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class VerifyLastSentIn(models.Model):
    user    = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name='last_sent')
    efforts = models.PositiveIntegerField()
    last_sent = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'verify code last sent in'
        verbose_name_plural = 'verify code last sent in'

class Customer(models.Model):
    name          = models.CharField(max_length=120)
    wallet        = models.FloatField(default=0)
    is_blocked    = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=11,unique=True)
    country_code  = models.CharField(max_length=6,verbose_name="كود الدولة",default='+20')
    def __str__(self):
        return self.name