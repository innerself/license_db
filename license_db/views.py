from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import OperationalError

from decouple import config

from .models import License, LicenseCategory, LicenseLocation


def auth(request, action='login'):
    if action == 'logout':
        logout(request)
        return redirect('license_db:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'login': {
            'prefix': config('LOGIN_PREFIX', default='DOMAIN\\'),
            'placeholder': config('LOGIN_PLACEHOLDER', default='Login'),
        },
        'access_denied': False,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('license_db:index')
        else:
            context['access_denied'] = True

    return render(request, 'license_db/auth.html', context)


def index(request):
    if request.user.is_anonymous:
        return redirect('license_db:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
    }

    lic_tree = {}
    for lic in License.objects.all():
        if lic.category.name not in lic_tree.keys():
            lic_tree[lic.category.name] = {}

        if lic.location.name not in lic_tree[lic.category.name].keys():
            lic_tree[lic.category.name][lic.location.name] = []

        lic_tree[lic.category.name][lic.location.name].append(lic)

    context['lic_tree'] = lic_tree

    return render(request, 'license_db/main.html', context)
