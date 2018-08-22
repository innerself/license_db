from django.shortcuts import render

from decouple import config

from .models import License


def index(request):
    context = {
        'logo': config('LOGO'),
        'licenses': dict(),
    }

    lic_types = set([
        value
        for item in License.objects.values('type')
        for _, value in item.items()
    ])

    for lic_type in lic_types:
        context['licenses'][lic_type] = License.objects.filter(
            type=lic_type,
        )

    return render(request, 'license_db/main.html', context)
