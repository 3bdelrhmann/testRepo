from django.urls import path
from .views import get_governorate,get_regions,resend_verify_code,lawyer_search

app_name = 'accounts'

urlpatterns = [
    path('lawyer/search/',lawyer_search,name='lawyer_search'),
    path('governorate/',get_governorate,name='governorate'),
    path('phone/resend/',resend_verify_code,name='resend'),
    path('regions/',get_regions,name='regions'),
]