from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def add_lead(request):
    return render(request, 'lead/add_lead.html')
