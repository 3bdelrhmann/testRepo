from django.urls import path
from . import views

app_name = 'phSessions'

urlpatterns = [
    path('',views.book_PhSession,name='book_phSession'),
    path('reviews/',views.get_lawyer_reviews,name='lw_reviews'),
]