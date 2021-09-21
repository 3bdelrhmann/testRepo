from django.urls import path
from . import views

app_name = 'phSessions'

urlpatterns = [
    # url('phone/lawyer/sessions',)
    path('lawyer/session/',views.lawyer_session,name='phlawyer_request'),
]