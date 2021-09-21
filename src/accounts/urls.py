from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('',views.user_home,name='user_home'),
    
    path('logout/'  ,auth_views.LogoutView.as_view(), name='logout'),
    path('login/'   ,views.login,name='login'),
    path('register/',views.register,name='register'),
    path('reset/'   ,views.reset_password,name='reset_password'),
    path('phone/review/',views.review_phone,name='review'),
    path('phone/verify/',views.verfiy_phone,name='verify'),
    
    # Lawyer profile 
    path('lw/<uuid:lawyer_id>/',views.lawyer_profile,name='lawyer_profile'),
    

]