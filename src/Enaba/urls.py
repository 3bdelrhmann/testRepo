from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls')),
    path('enaba/', include('settings.urls')),
    path('office/', include('office.urls')),
    path('phone/', include('phSessions.urls')),
    path('', home,name='home'),
    path('search/', search_results,name='search_results'),

    # REST Framework 
    path('api/accounts/', include('accounts.api.urls','accounts_api')), 
    path('api/office/'  , include('office.api.urls','office_api')), 
    path('api/phone/session/'  , include('phSessions.api.urls','phSession_api')), 

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
