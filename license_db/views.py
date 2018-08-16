from django.shortcuts import render

from .models import License


def index(request):
    licenses = License.objects.all()
    context = {'licenses': licenses}
    return render(request, 'license_db/main.html', context)

