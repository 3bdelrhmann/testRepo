import functools
from django.conf import settings
from django.shortcuts import redirect

 
def twofa_required(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.user.phone_verified:
            return view(request, *args, **kwargs)
        return redirect('accounts:verify')
    return wrapper

