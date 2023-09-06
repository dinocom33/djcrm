from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect


User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        organization = request.user.organizations.filter(members=request.user).get()
        return render(request, 'common/index.html', {'organization': organization})
    else:
        return render(request, 'common/index.html')
