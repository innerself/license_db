from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import OperationalError

from decouple import config

from .models import License, LicenseType


def auth(request):
    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'login': {
            'prefix': config('LOGIN_PREFIX', default='DOMAIN\\'),
            'placeholder': config('LOGIN_PLACEHOLDER', default='Login'),
        }
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect('/', user)
    else:
        return render(request, 'license_db/auth.html', context)


def auth_out(request):
    logout(request)
    return redirect('/')


def index(request):
    if request.user.is_anonymous:
        return redirect('license_db:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'licenses': dict(),
    }

    try:
        lic_types = set([
            value
            for item in LicenseType.objects.values('name')
            for _, value in item.items()
        ])
    except OperationalError:
        lic_types = set()

    for lic_type in lic_types:
        context['licenses'][lic_type] = License.objects.filter(
            type__name=lic_type,
        )

    return render(request, 'license_db/main.html', context)
