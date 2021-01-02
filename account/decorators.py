from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import  get_object_or_404
from account.models import Account 
from administration.models import Status

def account_user_required(function):
    def wrap(request, *args, **kwargs):
        account = get_object_or_404(Account, user=request.user)
        status = Status.objects.get(name="ACTIVE")
        if account is not None and account.status == status:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap