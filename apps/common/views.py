from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        organization = request.user.organizations.filter(members=request.user).first()
        return render(request, 'common/index.html', {'organization': organization})
    else:
        return render(request, 'common/index.html')


class ContactUsView(TemplateView):
    template_name = 'common/contact.html'


class AboutUsView(TemplateView):
    template_name = 'common/about.html'
