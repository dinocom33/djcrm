from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.common.forms import ContactForm
from djcrm.settings import CONTACT_FORM_EMAIL

User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        organization = request.user.organizations.filter(members=request.user).first()
        return render(request, 'common/index.html', {'organization': organization})
    else:
        return render(request, 'common/index.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["email"]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [CONTACT_FORM_EMAIL])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            form.save()

            return redirect('index')
    else:
        form = ContactForm()

    context = {
        'form': form
    }

    return render(request, 'common/contact.html', context)


class AboutUsView(TemplateView):
    template_name = 'common/about.html'
