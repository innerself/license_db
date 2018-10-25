from typing import List

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from decouple import config
from openpyxl import load_workbook

from license_db.handlers import save_to_disk
from license_db.utils import excel_columns, prepare_cell_value
from .models import License, ExcelEntry, LicenseCategory, LicenseLocation, LicenseType
from .forms import UploadFileForm


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
            return redirect('license_db:view')
        else:
            context['access_denied'] = True

    return render(request, 'license_db/auth.html', context)


def view(request):
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

    return render(request, 'license_db/view.html', context)


def parse_excel(file_path: str) -> List[ExcelEntry]:
    entries = []

    wb = load_workbook(file_path)
    ws = wb.active

    rows = ws.rows
    next(rows)  # skip header row

    for row in rows:
        entry = ExcelEntry(
            name=prepare_cell_value(row, 'name'),
            category=prepare_cell_value(row, 'category'),
            location=prepare_cell_value(row, 'location'),
            lic_type=prepare_cell_value(row, 'lic_type'),
            quantity=prepare_cell_value(row, 'quantity'),
            expires=prepare_cell_value(row, 'expires'),
            comment=prepare_cell_value(row, 'comment'),
        )

        entries.append(entry)

    return entries


def preview_import(request):
    saved_file_info = request.session['saved_file_info']
    entries = parse_excel(saved_file_info['path'])
    request.session['entries'] = entries

    lic_tree = {}
    for lic in entries:
        if lic.category not in lic_tree.keys():
            lic_tree[lic.category] = {}

        if lic.location not in lic_tree[lic.category].keys():
            lic_tree[lic.category][lic.location] = []

        lic_tree[lic.category][lic.location].append(lic)

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'lic_tree': lic_tree,
    }

    return render(request, 'license_db/import.html', context)


def submit_import(request) -> None:
    request.session['entries']: ExcelEntry
    entries = request.session['entries']

    for entry in entries:
        existing_category = LicenseCategory.objects.filter(
            name=entry.category
        )

        if existing_category:
            category = existing_category
        else:
            category = LicenseCategory(name=entry.category)
            category.save()

        existing_location = LicenseLocation.objects.filter(
            name=entry.location
        )

        if existing_location:
            location = existing_location
        else:
            location = LicenseLocation(name=entry.location)
            location.save()

        existing_type = LicenseType.objects.filter(
            name=entry.type
        )

        if existing_type:
            lic_type = existing_type
        else:
            lic_type = LicenseType(name=entry.type)
            lic_type.save()

        License.objects.create(
            name=entry.name,
            category=category,
            location=location,
            type=lic_type,
            quantity=entry.quantity,
            expires=entry.expires,
            comment=entry.comment,
        )

    return None


def import_data(request):
    if request.user.is_anonymous:
        return redirect('license_db:auth')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            saved_file_info = save_to_disk(request.FILES['file'])
            request.session['saved_file_info'] = saved_file_info

            preview_pressed = bool(request.POST.get('preview'))
            submit_pressed = bool(request.POST.get('submit'))

            if preview_pressed:
                return redirect('license_db:preview_import')

            if submit_pressed:
                submit_import(request)
    else:
        form = UploadFileForm()

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'form': form,
    }

    return render(request, 'license_db/import.html', context)
