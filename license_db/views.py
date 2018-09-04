from django.shortcuts import render

from decouple import config

from .models import License, LicenseType


def index(request):
    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'licenses': dict(),
    }

    lic_types = set([
        value
        for item in LicenseType.objects.values('name')
        for _, value in item.items()
    ])

    for lic_type in lic_types:
        context['licenses'][lic_type] = License.objects.filter(
            type__name=lic_type,
        )

    return render(request, 'license_db/main.html', context)
