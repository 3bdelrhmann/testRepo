from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display 	= ('email','register_date', 'last_login', 'in_review','is_staff')
    search_fields 	= ('email',)
    ordering= ('email',)
    readonly_fields =('register_date', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,CustomUserAdmin)
admin.site.register(Country)
admin.site.register(Governorate)
admin.site.register(Region)
admin.site.register(LawyerDegrees)
admin.site.register(VerifyLastSentIn)
admin.site.register(Specialties)
admin.site.register(Customer)