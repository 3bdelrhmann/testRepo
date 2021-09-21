from django.urls import path
from .views import privacy_and_terms

app_name = 'settings'

urlpatterns = [
    path('privacy/',privacy_and_terms,name='privacy_and_terms')
]