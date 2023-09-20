from django.http import Http404


def superuser_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper_func


def org_owner_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_org_owner:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper_func
